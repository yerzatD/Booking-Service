from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import hash_password
from ..models.User import User
from ..schemas.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate) -> User:
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = await self.db.get(User, user_id)
        if user is None:
            return None

        if user_update.username is not None:
            user.username = user_update.username
        if user_update.email is not None:
                    user.email = user_update.email 
        if user_update.password is not None:
            user.hashed_password = hash_password(user_update.password)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all_users(self) -> list[User]:
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalar_one_or_none()

    async def get_user_by_email(self,email : str) -> User | None:
         user = await self.db.execute(select(User).where(User.email == email))
         return user.scalar_one_or_none()