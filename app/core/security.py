from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.models import User
from app.db import get_db

SECRET_KEY: str = "change-me"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
ALGORITHM: str = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire.timestamp()}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)





async def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail = "could not validate credentials",
                                         headers={"WWW-Authenticate":"Bearer"},
                                         )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exeption
    except JWTError as e:
        raise credentials_exeption
    
    result= await db.exec(select(User).where(User.email == email))
    user = result.first()
    if user is None:
        raise credentials_exeption
    return user

    
