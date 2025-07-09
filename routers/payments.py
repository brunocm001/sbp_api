from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.payment import Payment, PaymentStatus
from models.order import Order
from schemas.payment import PaymentCreate, PaymentResponse, PaymentVerify
from utils.auth import get_current_admin
from models.admin import Admin

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initiate", response_model=PaymentResponse)
async def initiate_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    # Verify order exists
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if payment already exists for this order
    existing_payment = db.query(Payment).filter(Payment.order_id == payment.order_id).first()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this order")
    
    # Generate transaction ID (in production, this would come from payment gateway)
    import uuid
    transaction_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
    
    # Create payment
    db_payment = Payment(
        **payment.dict(),
        transaction_id=transaction_id,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    return db_payment

@router.post("/verify")
async def verify_payment(
    payment_verify: PaymentVerify,
    db: Session = Depends(get_db)
):
    # Find payment by transaction ID
    payment = db.query(Payment).filter(Payment.transaction_id == payment_verify.transaction_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # In production, this would verify with payment gateway
    # For demo purposes, we'll simulate a successful payment
    payment.status = PaymentStatus.PAID
    payment.paid_at = datetime.utcnow()
    
    # Update order status to in_progress
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if order:
        order.status = "in_progress"
        order.progress = "10%"
    
    db.commit()
    db.refresh(payment)
    
    return {
        "message": "Payment verified successfully",
        "payment": payment,
        "order_status": order.status if order else None
    }

# Admin endpoints
@router.get("/admin/", response_model=list[PaymentResponse])
async def get_payments_admin(
    skip: int = 0,
    limit: int = 100,
    status: PaymentStatus = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    payments = query.offset(skip).limit(limit).all()
    return payments

@router.put("/admin/{payment_id}/status")
async def update_payment_status(
    payment_id: str,
    status: PaymentStatus,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment.status = status
    if status == PaymentStatus.PAID and not payment.paid_at:
        payment.paid_at = datetime.utcnow()
    
    db.commit()
    db.refresh(payment)
    return {"message": "Payment status updated successfully", "payment": payment} 