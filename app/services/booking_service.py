from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.User import User
from ..repositories.booking_repository import BookingRepository
from ..schemas.schemas import BookingCreate, BookingRead, BookingUpdate
from .room_service import RoomService


class BookingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.booking_repository = BookingRepository(db)
        self.room_service = RoomService(db)

    async def create_booking(self, data: BookingCreate, current_user: User) -> BookingRead:
        available = await self.room_service.is_room_available_for_dates(
            data.room_id, data.check_in, data.check_out
        )
        if not available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is not available for the selected dates",
            )

        booking = await self.booking_repository.create_booking(data, current_user)
        if booking is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return BookingRead.model_validate(booking)

    async def update_booking(
        self, booking_id: int, data: BookingUpdate, current_user: User
    ) -> BookingRead:
        updated = await self.booking_repository.update_booking(booking_id, data, current_user)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return BookingRead.model_validate(updated)

    async def delete_booking(self, current_user: User, booking_id: int) -> dict:
        deleted = await self.booking_repository.delete_booking(current_user, booking_id)
        if deleted is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return deleted

    async def get_booking(self, current_user: User, booking_id: int) -> BookingRead:
        booking = await self.booking_repository.get_booking(booking_id, current_user)
        if booking is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return BookingRead.model_validate(booking)

    async def get_bookings(self, current_user: User) -> list[BookingRead]:
        bookings = await self.booking_repository.get_bookings_for_user(current_user)
        return [BookingRead.model_validate(b) for b in bookings]