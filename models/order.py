from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_type_id = Column(UUID(as_uuid=True), ForeignKey("service_types.id"), nullable=False)
    platform_id = Column(UUID(as_uuid=True), ForeignKey("platforms.id"), nullable=False)
    url = Column(String(500), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_total = Column(Float, nullable=False)
    email = Column(String(255), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    progress = Column(String(10), default="0%")  # e.g., "40%"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    service_type = relationship("ServiceType", back_populates="orders")
    platform = relationship("Platform")
    payments = relationship("Payment", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}', quantity={self.quantity})>" 