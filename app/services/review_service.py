from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.User import User
from ..repositories.review_repository import ReviewRepository
from ..schemas.schemas import ReviewCreate, ReviewRead, ReviewUpdate


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ReviewRepository(db)

    @staticmethod
    def _to_read(review) -> ReviewRead:
        return ReviewRead.model_validate(review)

    async def create_review(self, current_user: User, data: ReviewCreate) -> ReviewRead:
        review = await self.repo.create_review(current_user, data)
        return self._to_read(review)

    async def update_review(
        self, current_user: User, hotel_id: int, data: ReviewUpdate
    ) -> ReviewRead:
        review = await self.repo.update_review(current_user, hotel_id, data)
        if review is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return self._to_read(review)

    async def delete_review(self, current_user: User, hotel_id: int) -> dict:
        deleted = await self.repo.delete_review(current_user, hotel_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return {"message": "Review deleted"}

    async def get_all_reviews(self) -> list[ReviewRead]:
        reviews = await self.repo.get_all_reviews()
        return [self._to_read(r) for r in reviews]

    async def get_reviews_above_rating(self, rating: float = 4.0) -> list[ReviewRead]:
        reviews = await self.repo.get_reviews_above_rating(rating)
        return [self._to_read(r) for r in reviews]

    async def get_reviews_below_rating(self, rating: float = 4.0) -> list[ReviewRead]:
        reviews = await self.repo.get_reviews_below_rating(rating)
        return [self._to_read(r) for r in reviews]