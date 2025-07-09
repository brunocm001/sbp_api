from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"

class OrderBase(BaseModel):
    service_type_id: uuid.UUID
    platform_id: uuid.UUID
    url: HttpUrl
    quantity: int = Field(gt=0)
    email: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: uuid.UUID
    price_total: float
    status: OrderStatus
    progress: str
    created_at: datetime
    
    class Config:
        from_attributes = True 