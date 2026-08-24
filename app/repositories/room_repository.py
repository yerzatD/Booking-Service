from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import RoomRead
from ..models.Room import Room
from ..models.Hotel import Hotel
from ..schemas.enums import RoomType


class RoomRepository:
    def __init__(self,db : AsyncSession):
        self.db = db


    async def get_room_by_id(self,room_id : int):
        result = await self.db.execute(select(Room).where(Room.id == room_id))
        room = result.scalar_one_or_none()
        return room

    async def get_available_rooms(self,hotel_id : int):
        result = await self.db.execute(select(Room).where(Room.hotel_id == hotel_id,Room.is_available == True))
        rooms = result.scalars().all()
        return rooms


    async def get_rooms_price_between(self, min : float, max : float):
        result = await self.db.execute(select(Room).where(Room.price_per_night <= max,Room.price_per_night >= min))
        rooms = result.scalars().all()
        return rooms

    async def get_room_by_type(self, type : RoomType):
        result = await self.db.execute(select(Room).where(Room.room_type == type))
        rooms = result.scalars().all()
        return rooms

    

    
