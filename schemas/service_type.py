from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ServiceTypeBase(BaseModel):
    service_id: uuid.UUID
    name: str
    price_per_1000: float = Field(gt=0)
    min_quantity: int = Field(gt=0)
    max_quantity: int = Field(gt=0)
    delivery_time: str
    guarantee: bool = False
    description: Optional[str] = None
    is_active: bool = True

class ServiceTypeCreate(ServiceTypeBase):
    pass

class ServiceTypeUpdate(BaseModel):
    service_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    price_per_1000: Optional[float] = Field(None, gt=0)
    min_quantity: Optional[int] = Field(None, gt=0)
    max_quantity: Optional[int] = Field(None, gt=0)
    delivery_time: Optional[str] = None
    guarantee: Optional[bool] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceTypeResponse(ServiceTypeBase):
    id: uuid.UUID
    
    class Config:
        from_attributes = True 