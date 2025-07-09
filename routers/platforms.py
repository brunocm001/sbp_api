from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.platform import Platform
from schemas.platform import PlatformCreate, PlatformUpdate, PlatformResponse
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/admin/platforms", tags=["Admin - Platforms"])

@router.post("/", response_model=PlatformResponse)
async def create_platform(
    platform: PlatformCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    db_platform = Platform(**platform.dict())
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform

@router.get("/", response_model=List[PlatformResponse])
async def get_platforms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    platforms = db.query(Platform).offset(skip).limit(limit).all()
    return platforms

@router.get("/{platform_id}", response_model=PlatformResponse)
async def get_platform(
    platform_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform

@router.put("/{platform_id}", response_model=PlatformResponse)
async def update_platform(
    platform_id: str,
    platform_update: PlatformUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    update_data = platform_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(platform, field, value)
    
    db.commit()
    db.refresh(platform)
    return platform

@router.delete("/{platform_id}")
async def delete_platform(
    platform_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    db.delete(platform)
    db.commit()
    return {"message": "Platform deleted successfully"} 