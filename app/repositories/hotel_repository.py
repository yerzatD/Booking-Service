from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import HotelCreate, HotelUpdate
from ..models.Hotel import Hotel


class HotelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_hotel(self, hotel: HotelCreate) -> Hotel:
        new_hotel = Hotel(
            name=hotel.name,
            description=hotel.description,
            address=hotel.address,
            city=hotel.city,
            rating=hotel.rating,
            rooms_count=0,
        )
        self.db.add(new_hotel)
        await self.db.commit()
        await self.db.refresh(new_hotel)
        return new_hotel

    async def update_hotel(self, hotel_id: int, hotel: HotelUpdate) -> Hotel | None:
        existing = await self.get_hotel_by_id(hotel_id)
        if existing is None:
            return None

        if hotel.name is not None:
            existing.name = hotel.name
        if hotel.description is not None:
            existing.description = hotel.description
        if hotel.address is not None:
            existing.address = hotel.address
        if hotel.city is not None:
            existing.city = hotel.city
        if hotel.rating is not None:
            existing.rating = hotel.rating

        self.db.add(existing)
        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete_hotel(self, hotel_id: int) -> bool:
        existing = await self.get_hotel_by_id(hotel_id)
        if existing is None:
            return False

        await self.db.delete(existing)
        await self.db.commit()
        return True

    async def get_all_hotels(self):
        result = await self.db.execute(select(Hotel))
        hotels = result.scalars().all()
        return hotels

    async def get_hotel_by_name(self, name: str):
        result = await self.db.execute(select(Hotel).where(Hotel.name == name))
        hotel = result.scalar_one_or_none()
        return hotel

    async def get_hotels_by_city(self, city: str):
        result = await self.db.execute(select(Hotel).where(Hotel.city == city))
        hotels = result.scalars().all()
        return hotels

    async def get_hotels_with_good_rating(self):
        result = await self.db.execute(select(Hotel).where(Hotel.rating >= 4.5))
        hotels = result.scalars().all()
        return hotels

    async def get_hotel_by_id(self, hotel_id: int):
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()
        return hotel