from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.support_ticket import SupportTicket, TicketStatus
from schemas.support_ticket import SupportTicketCreate, SupportTicketUpdate, SupportTicketResponse
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/support", tags=["Support"])

@router.post("/", response_model=SupportTicketResponse)
async def create_support_ticket(
    ticket: SupportTicketCreate,
    db: Session = Depends(get_db)
):
    db_ticket = SupportTicket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# Admin endpoints
@router.get("/admin/", response_model=List[SupportTicketResponse])
async def get_support_tickets_admin(
    skip: int = 0,
    limit: int = 100,
    status: TicketStatus = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    query = db.query(SupportTicket)
    if status:
        query = query.filter(SupportTicket.status == status)
    tickets = query.offset(skip).limit(limit).all()
    return tickets

@router.get("/admin/{ticket_id}", response_model=SupportTicketResponse)
async def get_support_ticket_admin(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Support ticket not found")
    return ticket

@router.put("/admin/{ticket_id}", response_model=SupportTicketResponse)
async def update_support_ticket(
    ticket_id: str,
    ticket_update: SupportTicketUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Support ticket not found")
    
    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    # Update the updated_at timestamp
    from datetime import datetime
    ticket.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ticket)
    return ticket 