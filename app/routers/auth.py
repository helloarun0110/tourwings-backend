from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserRead, Token
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post('/register', response_model=UserRead)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.exec(select(User).where(User.email == payload.email))
    if q.first():
        raise HTTPException(status_code=400, detail="Email exists")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=get_password_hash(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post('/login', response_model=Token)
async def login(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.exec(select(User).where(User.email == payload.email))
    user = q.first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return Token(access_token=token)
