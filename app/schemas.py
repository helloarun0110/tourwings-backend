from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

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
