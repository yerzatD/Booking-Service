from ...database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer,index=True,primary_key=True)
    name = Column(String, index=True,nullable=False)
    description = Column(String,nullable=True)
    address = Column(String,nullable=False)
    city = Column(String,nullable=False)
    rating = Column(Float)
    rooms = Column(Integer)

    bookings = relationship("Booking", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="hotel", cascade="all, delete-orphan")
    