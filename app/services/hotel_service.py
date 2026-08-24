from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.Hotel import Hotel
from ..models.Room import Room
from ..repositories.hotel_repository import HotelRepository
from ..schemas.schemas import HotelRead


class HotelService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = HotelRepository(db)

    async def _rooms_count(self, hotel_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Room.id)).where(Room.hotel_id == hotel_id)
        )
        return result.scalar_one()

    async def _to_read(self, hotel: Hotel) -> HotelRead:
        rooms_count = await self._rooms_count(hotel.id)
        return HotelRead(
            id=hotel.id,
            name=hotel.name,
            description=hotel.description,
            address=hotel.address,
            city=hotel.city,
            rating=hotel.rating,
            rooms_count=rooms_count,
        )

    async def list_hotels(self) -> list[HotelRead]:
        hotels = await self.repo.get_all_hotels()
        return [await self._to_read(h) for h in hotels]

    async def get_hotel(self, hotel_id: int) -> HotelRead:
        hotel = await self.repo.get_hotel_by_id(hotel_id)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        return await self._to_read(hotel)

    async def get_hotel_by_name(self, name: str) -> HotelRead:
        hotel = await self.repo.get_hotel_by_name(name)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        return await self._to_read(hotel)

    async def get_hotels_by_city(self, city: str) -> list[HotelRead]:
        hotels = await self.repo.get_hotels_by_city(city)
        return [await self._to_read(h) for h in hotels]

    async def get_top_rated_hotels(self) -> list[HotelRead]:
        hotels = await self.repo.get_hotels_with_good_rating()
        return [await self._to_read(h) for h in hotels]