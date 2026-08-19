from ..models.User import User
from ..schemas.schemas import UserCreate,UserResponse,UserUpdate,Token
from ..auth import verify_password,create_access_token,hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status
from ..repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordRequestForm


class UserService:
    def __init__(self,db : AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def register_user(self,data : UserCreate) -> UserResponse:
        existing = await self.user_repository.get_user_by_username()
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User already registred")

        user = await self.user_repository.create_user(data)
        return UserResponse.model_validate(user)


    async def login_user(self,form_data : OAuth2PasswordRequestForm) -> Token:
        user = await self.user_repository.get_user_by_username(form_data.username)
        if user is None or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")

    async def update_me(self,data : UserUpdate) -> UserResponse:
        existing1 = await self.user_repository.get_user_by_username(data.username)
        existing2 = await self.user_repository.get_user_by_email(data.email)
        if existing1 is not None or existing2 is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this username or email already registred")
        user = await self.user_repository.update_user(data)
        return UserResponse.model_validate(user)

    async def get_info_about_me(self, current_user: User) -> UserResponse:
        user = await self.user_repository.get_user_by_id(current_user.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)


    
