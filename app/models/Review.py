from ...database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer,index=True,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    hotel_id = Column(Integer,ForeignKey("hotels.id"))
    rating = Column(Float)
    comment = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")
