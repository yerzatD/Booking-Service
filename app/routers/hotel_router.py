from fastapi import APIRouter, Depends
from ..services.hotel_service import HotelService
from ..schemas.schemas import HotelRead
from ..auth import get_current_user
from ..models.Hotel import Hotel
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from typing import List


router = APIRouter(prefix="/api/hotels",tags=['Hotel'])

async def get_hotel_service(db: AsyncSession = Depends(get_db)) -> HotelService:
    return HotelService(db)


@router.get('',response_model=List[HotelRead])
async def get_hotels(service : HotelService = Depends(get_hotel_service)):
    return await service.list_hotels()

@router.get("/by/id/{hotel_id}",response_model=HotelRead)
async def get_gotel_by_name(hotel_id : int,service : HotelService = Depends(get_hotel_service)):
    return await service.get_hotel(hotel_id)

@router.get('/by/name/{hotel_name}',response_model=HotelRead)
async def get_gotel_by_name(hotel_name : str,service : HotelService = Depends(get_hotel_service)):
    return await service.get_hotel_by_name(hotel_name)

@router.get("/gooodrating",response_model=List[HotelRead])
async def get_good_rating_hotels(service : HotelService = Depends(get_hotel_service)):
    return await service.get_top_rated_hotels()

@router.get("/by/city/{city_name}", response_model=List[HotelRead])
async def get_hotels_by_city(city_name: str, service: HotelService = Depends(get_hotel_service)):
    return await service.get_hotels_by_city(city_name)

