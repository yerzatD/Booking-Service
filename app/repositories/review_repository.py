from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.schemas import ReviewCreate,ReviewRead, ReviewUpdate
from ..models.Review import Review
from ..models.User import User


class ReviewRepository:
    def __init__(self,db : AsyncSession):
        self.db = db

    async def create_review(self,current_user : User, data : ReviewCreate):
        new_review = Review(
            user_id=current_user.id,
            hotel_id=data.hotel_id,
            rating=data.rating,
            comment=data.comment,
        )

        self.db.add(new_review)
        await self.db.commit()
        await self.db.refresh(new_review)
        return new_review

    async def update_review(self, current_user: User, hotel_id: int, data: ReviewUpdate):
        result = await self.db.execute(
            select(Review).where(Review.user_id == current_user.id, Review.hotel_id == hotel_id)
        )
        review = result.scalar_one_or_none()
        if review is None:
            return None

        if data.rating is not None:
            review.rating = data.rating
        if data.comment is not None:
            review.comment = data.comment

        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def delete_review(self, current_user: User, hotel_id: int) -> bool:
        result = await self.db.execute(
            select(Review).where(Review.user_id == current_user.id, Review.hotel_id == hotel_id)
        )
        review = result.scalar_one_or_none()
        if review is None:
            return False

        await self.db.delete(review)
        await self.db.commit()
        return True

    async def get_all_reviews(self):
        result = await self.db.execute(select(Review))
        reviews = result.scalars().all()
        return reviews

    async def get_reviews_above_rating(self, rating: float = 4.0):
        result = await self.db.execute(select(Review).where(Review.rating > rating))
        reviews = result.scalars().all()
        return reviews

    async def get_reviews_below_rating(self, rating: float = 4.0):
        result = await self.db.execute(select(Review).where(Review.rating < rating))
        reviews = result.scalars().all()
        return reviews
    