from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas import BookingCreate, BookingRead
from app.models import Booking, Tour
from app.db import get_db
from app.core.security import get_current_user
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors



router = APIRouter()

@router.post("/", response_model=BookingRead)
async def create_booking(
    booking_data: BookingCreate,
    db:AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.exec(select(Tour).where(Tour.id == booking_data.tour_id))
    tour = result.first()
    if not tour:
        raise HTTPException(status_code=404, detail="tour not found")
    
    total_price = tour.price * booking_data.persons

    booking = Booking(
        user_id = current_user.id,
        tour_id = tour.id,
        persons = booking_data.persons,
        age = booking_data.age,
        notes = booking_data.notes,
        total_price = total_price,
        
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    return booking



@router.get("/tour/{tour_id}", response_model = list[Booking])
async def get_bookings_for_tour(
    tour_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    tour = await db.get(Tour, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="tour not found")
    
    
    result = await db.exec(select(Booking).where(Booking.tour_id == tour_id))
    bookings = result.all()
    return bookings







@router.get("/tour/{tour_id}/export", response_class = FileResponse)
async def export_tour_bookings_pdf(tour_id: int, db: AsyncSession = Depends(get_db)):
    tour = await db.get(Tour, tour_id)
    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")
    
    result = await db.exec(select(Booking).where(Booking.tour_id == tour.id))
    bookings = result.all()

    if not bookings:
        raise HTTPException(status_code=404, detail="No booking found for this tour")
    
    filename = f"tour_{tour_id}_bookings.pdf"
    filepath = f"/tmp/{filename}"

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []


    elements.append(Paragraph(f"<b>Tour Name:</b> {tour.name}", None))
    elements.append(Paragraph(f"<b>Location:</b> {tour.location}", None))
    elements.append(Paragraph(f"<b>Date: </b> {tour.date}", None))
    elements.append(Spacer(1, 12))

    data = [["User ID", "Persons", "Total Price", "Booking Date", "Status"]]
    for b in bookings:
        data.append([
            b.user_id,
            b.persons,
            f"{b.total_price} BTD",
            b.booking_date.strftime("%Y-%m-%d"),
            b.status
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0),colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))


    elements.append(table)
    doc.build(elements)

    return FileResponse(filepath, filename=filename)