# app/models.py
from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    role: str = Field(default="user")
    full_name: Optional[str] = None

    bookings: List["Booking"] = Relationship(back_populates="user")


class Tour(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: date
    price: float
    location: str
    image: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    bookings: List["Booking"] = Relationship(back_populates="tour")


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    tour_id: int = Field(foreign_key="tour.id")
    persons: int
    age: Optional[int] = None
    notes: Optional[str] = None
    total_price: float
    booking_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="confirmed")
    qr_token: Optional[str] = None

    user: Optional[User] = Relationship(back_populates="bookings")
    tour: Optional[Tour] = Relationship(back_populates="bookings")
