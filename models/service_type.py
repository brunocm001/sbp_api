from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from database import Base

class ServiceType(Base):
    __tablename__ = "service_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price_per_1000 = Column(Float, nullable=False)
    min_quantity = Column(Integer, nullable=False)
    max_quantity = Column(Integer, nullable=False)
    delivery_time = Column(String(100), nullable=False)  # e.g., "24-48 hours"
    guarantee = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    service = relationship("Service", back_populates="service_types")
    orders = relationship("Order", back_populates="service_type")
    
    def __repr__(self):
        return f"<ServiceType(id={self.id}, name='{self.name}', service_id={self.service_id})>" 