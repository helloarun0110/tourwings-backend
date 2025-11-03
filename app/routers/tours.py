from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_db
from app.models import Tour
from app.schemas import TourCreate, TourRead
from app.deps import get_current_admin

router = APIRouter()

# @router.get('/', response_model=List[TourRead])
# async def list_tours(db: AsyncSession = Depends(get_db)):
#     stmt = select(Tour).order_by(Tour.date)
#     res = await db.exec(stmt)
#     return res.all()

@router.post('/', response_model=TourRead, status_code=status.HTTP_201_CREATED)
async def create_tour(payload: TourCreate, db: AsyncSession = Depends(get_db), admin = Depends(get_current_admin)):
    tour = Tour(**payload.model_dump())
    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    return tour

@router.delete('/{tour_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tour(tour_id: int, db: AsyncSession = Depends(get_db), admin = Depends(get_current_admin)):
    tour = await db.get(Tour, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail='Not found')
    await db.delete(tour)
    await db.commit()
    return None















from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db import get_db
from app.models import Tour
from app.schemas import TourCreate, TourRead
from app.deps import get_current_admin




@router.get('/', response_model=List[TourRead])
async def list_tours(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by name or location"),
    sort: str = Query("dateAsc", description="Sort: dateAsc, dateDesc, priceAsc, priceDesc, nameAsc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(6, ge=1, le=50),
):
    stmt = select(Tour)

    # --- Filter by search ---
    if search:
        stmt = stmt.where(
            (Tour.name.ilike(f"%{search}%")) | (Tour.location.ilike(f"%{search}%"))
        )

    # --- Sorting ---
    if sort == "dateAsc":
        stmt = stmt.order_by(Tour.date.asc())
    elif sort == "dateDesc":
        stmt = stmt.order_by(Tour.date.desc())
    elif sort == "priceAsc":
        stmt = stmt.order_by(Tour.price.asc())
    elif sort == "priceDesc":
        stmt = stmt.order_by(Tour.price.desc())
    elif sort == "nameAsc":
        stmt = stmt.order_by(Tour.name.asc())

    # --- Execute ---
    res = await db.exec(stmt)
    all_tours = res.all()

    # --- Pagination ---
    start = (page - 1) * per_page
    end = start + per_page
    paginated = all_tours[start:end]

    return paginated
