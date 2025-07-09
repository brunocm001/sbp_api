from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ServiceBase(BaseModel):
    platform_id: uuid.UUID
    name: str
    description: Optional[str] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    platform_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True 