from ..database import Base
from sqlalchemy import Column,String,Integer,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer,index=True,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    hotel_id = Column(Integer,ForeignKey("hotels.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(DateTime,default=datetime.utcnow)
    check_out = Column(DateTime)
    guests = Column(Integer)
    total_price = Column(Float)
    status = Column(String)

    user = relationship("User", back_populates="bookings")
    hotel = relationship("Hotel", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")