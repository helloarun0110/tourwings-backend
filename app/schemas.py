from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

class TourCreate(BaseModel):
    name: str
    date: date
    price: float
    location: str
    image: Optional[str] = None
    description: Optional[str] = None

class TourRead(BaseModel):
    id: int
    name: str
    date: date
    price: float
    location: str
    image: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True



class BookingCreate(BaseModel):
    tour_id: int
    persons: int
    age: int | None = None
    notes: str | None = None


class BookingRead(BaseModel):
    id: int
    tour_id : int
    user_id : int
    persons: int
    total_price: float
    booking_date: datetime
    status: str

    class Config:
        orm_mode = True
        
