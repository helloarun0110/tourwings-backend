from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_db
from sqlmodel import select
from app.models import User

async def get_current_admin(db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(User).where(User.role == "admin"))
    admin = result.first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return admin
