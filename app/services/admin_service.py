from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.booking_repository import BookingRepository
from ..repositories.hotel_repository import HotelRepository
from ..repositories.room_repository import RoomRepository
from ..repositories.user_repository import UserRepository
from ..schemas.schemas import (
    BookingRead,
    HotelCreate,
    HotelRead,
    HotelUpdate,
    RoomCreate,
    RoomRead,
    RoomUpdate,
    UserResponseForAdmin,
)


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.hotel_repository = HotelRepository(db)
        self.room_repository = RoomRepository(db)
        self.booking_repository = BookingRepository(db)
        self.user_repository = UserRepository(db)

    # ---------- Hotels ----------

    async def create_hotel(self, data: HotelCreate) -> HotelRead:
        hotel = await self.hotel_repository.create_hotel(data)
        return HotelRead.model_validate(hotel)

    async def update_hotel(self, hotel_id: int, data: HotelUpdate) -> HotelRead:
        hotel = await self.hotel_repository.update_hotel(hotel_id, data)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        return HotelRead.model_validate(hotel)

    async def delete_hotel(self, hotel_id: int) -> dict:
        deleted = await self.hotel_repository.delete_hotel(hotel_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        return {"message": "Hotel deleted"}

    # ---------- Rooms ----------

    async def create_room(self, data: RoomCreate) -> RoomRead:
        hotel = await self.hotel_repository.get_hotel_by_id(data.hotel_id)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
        room = await self.room_repository.create_room(data)
        return RoomRead.model_validate(room)

    async def update_room(self, room_id: int, data: RoomUpdate) -> RoomRead:
        room = await self.room_repository.update_room(room_id, data)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return RoomRead.model_validate(room)

    async def delete_room(self, room_id: int) -> dict:
        deleted = await self.room_repository.delete_room(room_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return {"message": "Room deleted"}

    # ---------- Users ----------

    async def list_users(self) -> list[UserResponseForAdmin]:
        users = await self.user_repository.get_all_users()
        return [UserResponseForAdmin.model_validate(u) for u in users]

    # ---------- Bookings ----------

    async def list_all_bookings(self) -> list[BookingRead]:
        bookings = await self.booking_repository.get_all_bookings()
        return [BookingRead.model_validate(b) for b in bookings]