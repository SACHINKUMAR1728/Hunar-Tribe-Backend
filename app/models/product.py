from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image_url = Column(String(512))
    description = Column(Text)
    swiggy_mart_link = Column(String(512), nullable=False)
    price = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())