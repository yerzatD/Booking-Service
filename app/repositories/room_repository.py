from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.Hotel import Hotel
from ..models.Room import Room
from ..schemas.enums import RoomType
from ..schemas.schemas import RoomCreate, RoomUpdate


class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_room(self, room: RoomCreate) -> Room:
        new_room = Room(
            hotel_id=room.hotel_id,
            room_number=room.room_number,
            room_type=room.room_type,
            price_per_night=room.price_per_night,
            capacity=room.capacity,
            description=room.description,
            is_available=True,
        )
        self.db.add(new_room)
        await self.db.commit()
        await self.db.refresh(new_room)
        return new_room

    async def update_room(self, room_id: int, room: RoomUpdate) -> Room | None:
        existing = await self.get_room_by_id(room_id)
        if existing is None:
            return None

        if room.room_number is not None:
            existing.room_number = room.room_number
        if room.room_type is not None:
            existing.room_type = room.room_type
        if room.price_per_night is not None:
            existing.price_per_night = room.price_per_night
        if room.capacity is not None:
            existing.capacity = room.capacity
        if room.description is not None:
            existing.description = room.description
        if room.is_available is not None:
            existing.is_available = room.is_available

        self.db.add(existing)
        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete_room(self, room_id: int) -> bool:
        existing = await self.get_room_by_id(room_id)
        if existing is None:
            return False

        await self.db.delete(existing)
        await self.db.commit()
        return True

    async def get_room_by_id(self, room_id: int, hotel_id: int):
        result = await self.db.execute(
            select(Room).where(Room.id == room_id, Room.hotel_id == hotel_id)
        )
        return result.scalar_one_or_none()

    async def get_available_rooms(self, hotel_id: int):
        result = await self.db.execute(
            select(Room).where(Room.hotel_id == hotel_id, Room.is_available == True)
        )
        rooms = result.scalars().all()
        return rooms

    async def get_rooms_price_between(self, min: float, max: float):
        result = await self.db.execute(
            select(Room).where(Room.price_per_night <= max, Room.price_per_night >= min)
        )
        rooms = result.scalars().all()
        return rooms

    async def get_room_by_type(self, type: RoomType):
        result = await self.db.execute(select(Room).where(Room.room_type == type))
        rooms = result.scalars().all()
        return rooms

    async def get_room_by_id_plain(self, room_id: int):
        result = await self.db.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none()