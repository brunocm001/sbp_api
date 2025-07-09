from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
import uuid

class PlatformBase(BaseModel):
    name: str
    icon_url: Optional[HttpUrl] = None
    is_active: bool = True

class PlatformCreate(PlatformBase):
    pass

class PlatformUpdate(BaseModel):
    name: Optional[str] = None
    icon_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None

class PlatformResponse(PlatformBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True 