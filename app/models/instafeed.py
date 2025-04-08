from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class InstaFeed(Base):
    __tablename__ = "instafeeds"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String(512), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author = relationship("User", back_populates="instafeeds")

