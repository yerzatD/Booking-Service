from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import BookingCreate, BookingUpdate
from ..models.Booking import Booking
from ..models.Room import Room
from ..models.User import User


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_booking(self, booking: BookingCreate, current_user: User) -> Booking | None:
        room_result = await self.db.execute(select(Room).where(Room.id == booking.room_id))
        room = room_result.scalar_one_or_none()
        if room is None:
            return None

        nights = (booking.check_out - booking.check_in).days
        total_price = room.price_per_night * max(nights, 1)

        new_booking = Booking(
            user_id=current_user.id,
            hotel_id=booking.hotel_id,
            room_id=booking.room_id,
            check_in=booking.check_in,
            check_out=booking.check_out,
            guests=booking.guests,
            total_price=total_price,
            status="pending",
        )

        self.db.add(new_booking)
        await self.db.commit()
        await self.db.refresh(new_booking)
        return new_booking

    async def update_booking(self, booking_id: int, booking: BookingUpdate, current_user: User) -> Booking | None:
        result = await self.db.execute(
            select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
        )
        existing = result.scalar_one_or_none()
        if existing is None:
            return None

        if booking.status is not None:
            existing.status = booking.status

        self.db.add(existing)
        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def delete_booking(self, current_user: User, booking_id: int) -> dict | None:
        result = await self.db.execute(
            select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
        )
        existing = result.scalar_one_or_none()
        if existing is None:
            return None

        await self.db.delete(existing)
        await self.db.commit()
        return {"message": "Booking deleted"}

    async def get_booking(self, booking_id: int, current_user: User) -> Booking | None:
        result = await self.db.execute(
            select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
        )
        return result.scalar_one_or_none()

    async def get_bookings_for_user(self, current_user: User) -> list[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.user_id == current_user.id))
        return result.scalars().all()