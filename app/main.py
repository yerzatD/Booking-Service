from fastapi import FastAPI
from .routers import (admin_router,
                      booking_router,
                      hotel_router,
                      room_router,
                      user_router,
                      review_router,)

from .database import Base
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan,title="Hotel Booking Service")

app.include_router(admin_router)
app.include_router(booking_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(user_router)
app.include_router(review_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
