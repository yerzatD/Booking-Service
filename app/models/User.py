from ..database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,index=True,primary_key=True)
    username = Column(String, index=True)
    email = Column(String,index=True,unique=True)
    hashed_password = Column(String)
    role = Column(String,default="user")
    is_active = Column(Boolean, default="True")
    created_at = Column(DateTime,default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")