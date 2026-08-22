from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import HotelRead,HotelCreate,HotelUpdate
from ..models.Hotel import Hotel

class HotelRepository:
    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_all_hotels(self) -> list[HotelRead]:
        result = await self.db.execute(select(Hotel))
        hotels = result.scalars().all()
        return [HotelRead.model_validate(hotel) for hotel in hotels]

    async def get_hotel_by_name(self,name : str) -> HotelRead:
        result = await self.db.execute(select(Hotel).where(Hotel.name == name))
        hotel = result.scalar_one_or_none()
        return HotelRead.model_validate(hotel) if hotel else None

    async def get_hotels_by_city(self,city : str) -> list[HotelRead]:
        result = await self.db.execute(select(Hotel).where(Hotel.city == city))
        hotels = result.scalars().all()
        return [HotelRead.model_validate(hotel) for hotel in hotels]

    async def get_hotels_with_good_rating(self) -> list[HotelRead]:
        result = await self.db.execute(select(Hotel).where(Hotel.rating >= 4.5))
        hotels = result.scalars().all()
        return [HotelRead.model_validate(hotel) for hotel in hotels]

    async def get_hotel_by_id(self, hotel_id : int) -> HotelRead:
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()
        return HotelRead.model_validate(hotel)

    

    
