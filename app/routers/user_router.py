from fastapi import APIRouter, Depends
from ..services.user_service import UserService
from ..schemas.schemas import UserCreate,UserResponse,UserUpdate,Token
from ..auth import get_current_user
from ..models.User import User
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db

router = APIRouter(prefix="/api/users",tags=["Users"])

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.register_user(data)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    return await service.login_user(form_data)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update_me(current_user, data)