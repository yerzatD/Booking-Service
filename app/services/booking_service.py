from ..schemas.schemas import BookingCreate,BookingRead,BookingUpdate
from ..models.Booking import Booking
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException,status
from ..models.Hotel import Hotel
from ..models.Room import Room



class BookingService:
    def __init__(self,db : AsyncSession):
        self.db = db

    async def create_booking(self,data : BookingCreate,user_id : int):
        room = await self.db
