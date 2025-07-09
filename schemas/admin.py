from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class AdminRole(str, Enum):
    SUPERADMIN = "superadmin"
    MODERATOR = "moderator"

class AdminBase(BaseModel):
    email: EmailStr
    role: AdminRole = AdminRole.MODERATOR

class AdminCreate(AdminBase):
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(AdminBase):
    id: uuid.UUID
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True 