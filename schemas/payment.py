from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class PaymentMethod(str, Enum):
    ORANGE_MONEY = "orange_money"
    CARD = "card"
    MOBILE_MONEY = "mobile_money"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"

class PaymentBase(BaseModel):
    order_id: uuid.UUID
    method: PaymentMethod
    phone_number: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: uuid.UUID
    transaction_id: Optional[str] = None
    status: PaymentStatus
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentVerify(BaseModel):
    transaction_id: str 