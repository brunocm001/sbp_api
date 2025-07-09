from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    RESPONDED = "responded"
    CLOSED = "closed"

class SupportTicketBase(BaseModel):
    email: EmailStr
    message: str

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    response: Optional[str] = None

class SupportTicketResponse(SupportTicketBase):
    id: uuid.UUID
    status: TicketStatus
    response: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 