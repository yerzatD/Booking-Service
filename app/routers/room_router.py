from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.enums import RoomType
from ..schemas.schemas import RoomRead
from ..services.room_service import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])


def get_room_service(db: AsyncSession = Depends(get_db)) -> RoomService:
    return RoomService(db)


@router.get("/{hotel_id:int}/{room_id:int}", response_model=RoomRead)
async def get_room(
    hotel_id: int,
    room_id: int,
    service: RoomService = Depends(get_room_service),
) -> RoomRead:
    return await service.get_room(hotel_id, room_id)


@router.get("/hotel/{hotel_id}/available", response_model=list[RoomRead])
async def get_available_rooms(
    hotel_id: int,
    service: RoomService = Depends(get_room_service),
) -> list[RoomRead]:
    return await service.get_available_rooms(hotel_id)


@router.get("/filter/price", response_model=list[RoomRead])
async def get_rooms_by_price_range(
    min_price: float = Query(..., ge=0),
    max_price: float = Query(..., ge=0),
    service: RoomService = Depends(get_room_service),
) -> list[RoomRead]:
    return await service.get_rooms_by_price_range(min_price, max_price)


@router.get("/filter/type", response_model=list[RoomRead])
async def get_rooms_by_type(
    room_type: RoomType,
    service: RoomService = Depends(get_room_service),
) -> list[RoomRead]:
    return await service.get_rooms_by_type(room_type)


@router.get("/{room_id:int}/availability", response_model=bool)
async def is_room_available_for_dates(
    room_id: int,
    check_in: datetime,
    check_out: datetime,
    service: RoomService = Depends(get_room_service),
) -> bool:
    return await service.is_room_available_for_dates(room_id, check_in, check_out)