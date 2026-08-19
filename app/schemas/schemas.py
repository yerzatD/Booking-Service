from pydantic import BaseModel,Field,EmailStr,ConfigDict
from typing import Optional,List
from datetime import datetime

# ==================== USER ====================
class UserBase(BaseModel):
    username : str = Field(...,min_length=3,max_length=30)
    email : EmailStr
    password : str = Field(...,min_length=7)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username : Optional[str] = None
    email : Optional[EmailStr] = None
    password : Optional[str] = None

class UserResponseForAdmin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int
    username : str
    email : str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username : str
    email : str

# ==================== HOTEL ====================
 
class HotelBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    rating: Optional[float] = Field(default=None, ge=0, le=5)
 
 
class HotelCreate(HotelBase):
    pass
 
 
class HotelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
 
 
class HotelRead(HotelBase):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    rooms_count: Optional[int] = None
 
 
# ==================== ROOM ====================
 
class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price_per_night: float = Field(gt=0)
    capacity: int = Field(gt=0)
    description: Optional[str] = None
 
 
class RoomCreate(RoomBase):
    hotel_id: int
 
 
class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price_per_night: Optional[float] = Field(default=None, gt=0)
    capacity: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None
    is_available: Optional[bool] = None
 
 
class RoomRead(RoomBase):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    hotel_id: int
    is_available: bool
 
 
# ==================== BOOKING ====================
 
class BookingBase(BaseModel):
    hotel_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    guests: int = Field(gt=0)
 
 
class BookingCreate(BookingBase):
    pass
 
 
class BookingUpdate(BaseModel):
    status: Optional[str] = None
 
 
class BookingRead(BookingBase):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    user_id: int
    total_price: float
    status: str
 
 
# ==================== REVIEW ====================
 
class ReviewBase(BaseModel):
    hotel_id: int
    rating: float = Field(ge=1, le=5)
    comment: Optional[str] = None
 
 
class ReviewCreate(ReviewBase):
    pass
 
 
class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
 
 
class ReviewRead(ReviewBase):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    user_id: int
    created_at: datetime
 

