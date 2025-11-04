from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import init_models
from app.routers import auth, users, tours, booking
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(title = "TourWins", lifespan = lifespan)


from fastapi.staticfiles import StaticFiles

app.mount("/image", StaticFiles(directory="app/image"), name="image")


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    
)



app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tours.router, prefix="/tours", tags=["tours"])

app.include_router(booking.router, prefix="/booking", tags=["booking"])