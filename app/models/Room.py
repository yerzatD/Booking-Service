from ..database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer,index=True,primary_key=True)
    hotel_id = Column(Integer,ForeignKey("hotels.id"))
    room_number = Column(String,nullable=False)
    room_type = Column(String,nullable=False)
    price_per_night = Column(Float,nullable=False)
    capacity = Column(Integer,nullable=False)
    description = Column(String)
    is_available = Column(Boolean,default="True")

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

