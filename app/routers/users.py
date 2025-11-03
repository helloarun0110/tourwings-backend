from fastapi import APIRouter, Depends
from app.schemas import UserRead
from app.deps import get_current_admin
from app.models import User

router = APIRouter()

@router.get('/me', response_model=UserRead)
async def me(admin: User = Depends(get_current_admin)):
    return admin
