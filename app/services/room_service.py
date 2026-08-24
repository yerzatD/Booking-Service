from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.Booking import Booking
from ..models.Room import Room
from ..repositories.room_repository import RoomRepository
from ..schemas.enums import RoomType
from ..schemas.schemas import RoomRead


class RoomService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = RoomRepository(db)

    @staticmethod
    def _to_read(room: Room) -> RoomRead:
        return RoomRead.model_validate(room)

    async def get_room(self, room_id: int) -> RoomRead:
        room = await self.repo.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return self._to_read(room)

    async def get_available_rooms(self, hotel_id: int) -> list[RoomRead]:
        rooms = await self.repo.get_available_rooms(hotel_id)
        return [self._to_read(r) for r in rooms]

    async def get_rooms_by_price_range(self, min_price: float, max_price: float) -> list[RoomRead]:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_price cannot be greater than max_price",
            )
        rooms = await self.repo.get_rooms_price_between(min_price, max_price)
        return [self._to_read(r) for r in rooms]

    async def get_rooms_by_type(self, room_type: RoomType) -> list[RoomRead]:
        rooms = await self.repo.get_room_by_type(room_type)
        return [self._to_read(r) for r in rooms]

    async def is_room_available_for_dates(
        self, room_id: int, check_in: datetime, check_out: datetime) -> bool:

        room = await self.repo.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        if not room.is_available:
            return False

        result = await self.db.execute(
            select(Booking).where(
                Booking.room_id == room_id,
                Booking.status != "cancelled",
                Booking.check_in < check_out,
                Booking.check_out > check_in,
            )
        )
        conflicting = result.scalars().first()
        return conflicting is None