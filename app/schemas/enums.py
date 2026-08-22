from enum import Enum

class RoomType(str, Enum):
    single = "single"
    double = "double"
    twin = "twin"
    suite = "suite"
    deluxe = "deluxe"


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

