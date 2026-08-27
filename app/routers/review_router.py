from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..auth import get_current_user
from ..models.User import User
from ..schemas.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from ..services.review_service import ReviewService

router = APIRouter(prefix="/reviews", tags=["Reviews"])


def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.post("", response_model=ReviewRead, status_code=201)
async def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
) -> ReviewRead:
    return await service.create_review(current_user, data)


@router.patch("/{hotel_id}", response_model=ReviewRead)
async def update_review(
    hotel_id: int,
    data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
) -> ReviewRead:
    return await service.update_review(current_user, hotel_id, data)


@router.delete("/{hotel_id}")
async def delete_review(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
) -> dict:
    return await service.delete_review(current_user, hotel_id)


@router.get("", response_model=list[ReviewRead])
async def get_all_reviews(
    service: ReviewService = Depends(get_review_service),
) -> list[ReviewRead]:
    return await service.get_all_reviews()


@router.get("/above", response_model=list[ReviewRead])
async def get_reviews_above_rating(
    rating: float = Query(4.0, ge=0, le=5),
    service: ReviewService = Depends(get_review_service),
) -> list[ReviewRead]:
    return await service.get_reviews_above_rating(rating)


@router.get("/below", response_model=list[ReviewRead])
async def get_reviews_below_rating(
    rating: float = Query(4.0, ge=0, le=5),
    service: ReviewService = Depends(get_review_service),
) -> list[ReviewRead]:
    return await service.get_reviews_below_rating(rating)