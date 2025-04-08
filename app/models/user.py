from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    blogs = relationship("Blog", back_populates="author")
    instafeeds = relationship("InstaFeed", back_populates="author")
    
