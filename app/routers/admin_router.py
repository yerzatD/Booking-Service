from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..auth import require_admin
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
from ..services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(db)


# ---------- Hotels ----------

@router.post("/hotels", response_model=HotelRead, status_code=201)
async def create_hotel(
    data: HotelCreate,
    service: AdminService = Depends(get_admin_service),
) -> HotelRead:
    return await service.create_hotel(data)


@router.patch("/hotels/{hotel_id}", response_model=HotelRead)
async def update_hotel(
    hotel_id: int,
    data: HotelUpdate,
    service: AdminService = Depends(get_admin_service),
) -> HotelRead:
    return await service.update_hotel(hotel_id, data)


@router.delete("/hotels/{hotel_id}")
async def delete_hotel(
    hotel_id: int,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    return await service.delete_hotel(hotel_id)


# ---------- Rooms ----------

@router.post("/rooms", response_model=RoomRead, status_code=201)
async def create_room(
    data: RoomCreate,
    service: AdminService = Depends(get_admin_service),
) -> RoomRead:
    return await service.create_room(data)


@router.patch("/rooms/{room_id}", response_model=RoomRead)
async def update_room(
    room_id: int,
    data: RoomUpdate,
    service: AdminService = Depends(get_admin_service),
) -> RoomRead:
    return await service.update_room(room_id, data)


@router.delete("/rooms/{room_id}")
async def delete_room(
    room_id: int,
    service: AdminService = Depends(get_admin_service),
) -> dict:
    return await service.delete_room(room_id)


# ---------- Users ----------

@router.get("/users", response_model=list[UserResponseForAdmin])
async def list_users(
    service: AdminService = Depends(get_admin_service),
) -> list[UserResponseForAdmin]:
    return await service.list_users()


# ---------- Bookings ----------

@router.get("/bookings", response_model=list[BookingRead])
async def list_all_bookings(
    service: AdminService = Depends(get_admin_service),
) -> list[BookingRead]:
    return await service.list_all_bookings()