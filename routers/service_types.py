from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.service_type import ServiceType
from models.service import Service
from schemas.service_type import ServiceTypeCreate, ServiceTypeUpdate, ServiceTypeResponse
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/admin/service-types", tags=["Admin - Service Types"])

@router.post("/", response_model=ServiceTypeResponse)
async def create_service_type(
    service_type: ServiceTypeCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    # Verify service exists
    service = db.query(Service).filter(Service.id == service_type.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Validate quantity range
    if service_type.min_quantity >= service_type.max_quantity:
        raise HTTPException(status_code=400, detail="min_quantity must be less than max_quantity")
    
    db_service_type = ServiceType(**service_type.dict())
    db.add(db_service_type)
    db.commit()
    db.refresh(db_service_type)
    return db_service_type

@router.get("/", response_model=List[ServiceTypeResponse])
async def get_service_types(
    skip: int = 0,
    limit: int = 100,
    service_id: str = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    query = db.query(ServiceType)
    if service_id:
        query = query.filter(ServiceType.service_id == service_id)
    service_types = query.offset(skip).limit(limit).all()
    return service_types

@router.get("/{service_type_id}", response_model=ServiceTypeResponse)
async def get_service_type(
    service_type_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if service_type is None:
        raise HTTPException(status_code=404, detail="Service type not found")
    return service_type

@router.put("/{service_type_id}", response_model=ServiceTypeResponse)
async def update_service_type(
    service_type_id: str,
    service_type_update: ServiceTypeUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if service_type is None:
        raise HTTPException(status_code=404, detail="Service type not found")
    
    # Verify service exists if service_id is being updated
    if service_type_update.service_id:
        service = db.query(Service).filter(Service.id == service_type_update.service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
    
    # Validate quantity range if being updated
    if service_type_update.min_quantity and service_type_update.max_quantity:
        if service_type_update.min_quantity >= service_type_update.max_quantity:
            raise HTTPException(status_code=400, detail="min_quantity must be less than max_quantity")
    
    update_data = service_type_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service_type, field, value)
    
    db.commit()
    db.refresh(service_type)
    return service_type

@router.delete("/{service_type_id}")
async def delete_service_type(
    service_type_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if service_type is None:
        raise HTTPException(status_code=404, detail="Service type not found")
    
    db.delete(service_type)
    db.commit()
    return {"message": "Service type deleted successfully"} 