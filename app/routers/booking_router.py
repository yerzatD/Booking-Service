from fastapi import APIRouter,Depends
from ..services.booking_service import BookingService
from ..auth import get_current_user
from ..models.User import User
from ..schemas.schemas import BookingCreate,BookingRead,BookingUpdate
from typing import Optional,List
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_booking_service(db : AsyncSession = Depends(get_db)):
    return BookingService(db)

router = APIRouter(tags=['Booking'],prefix="/api/bookings")

@router.put('/create',response_model=BookingRead)
async def create_booking(data : BookingCreate,current_user : User = Depends(get_current_user),service : BookingService = Depends(get_booking_service)):
    return await service.create_booking(data,current_user)

@router.patch('/update/{booking_id}',response_model=BookingRead)
async def update_booking(booking_id : int,data : BookingUpdate,current_user : User = Depends(get_current_user),service : BookingService = Depends(get_booking_service)):
    return await service.update_booking(booking_id,data,current_user)

@router.delete('/delete/{booking_id}')
async def delete_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> dict:
    return await service.delete_booking(current_user, booking_id)

@router.get('/{booking_id}',response_model=BookingRead)
async def get_booking(booking_id:int,current_user : User = Depends(get_current_user),service : BookingService = Depends(get_booking_service)):
    return await service.get_booking(current_user,booking_id)

@router.get('',response_model=List[BookingRead])
async def get_booking(current_user : User = Depends(get_current_user),service : BookingService = Depends(get_booking_service)):
    return await service.get_bookings(current_user)