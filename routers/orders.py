from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderStatus
from models.service_type import ServiceType
from models.platform import Platform
from schemas.order import OrderCreate, OrderResponse
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    # Verify service type exists and is active
    service_type = db.query(ServiceType).filter(
        ServiceType.id == order.service_type_id,
        ServiceType.is_active == True
    ).first()
    if not service_type:
        raise HTTPException(status_code=404, detail="Service type not found or inactive")
    
    # Verify platform exists
    platform = db.query(Platform).filter(
        Platform.id == order.platform_id,
        Platform.is_active == True
    ).first()
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found or inactive")
    
    # Validate quantity
    if order.quantity < service_type.min_quantity or order.quantity > service_type.max_quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Quantity must be between {service_type.min_quantity} and {service_type.max_quantity}"
        )
    
    # Calculate total price
    price_total = (order.quantity / 1000) * service_type.price_per_1000
    
    # Create order
    db_order = Order(
        **order.dict(),
        price_total=price_total,
        status=OrderStatus.PENDING,
        progress="0%"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Admin endpoints
@router.get("/admin/", response_model=List[OrderResponse])
async def get_orders_admin(
    skip: int = 0,
    limit: int = 100,
    status: OrderStatus = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.put("/admin/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: OrderStatus,
    progress: str = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    if progress:
        order.progress = progress
    
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated successfully", "order": order} 