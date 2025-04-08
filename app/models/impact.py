from sqlalchemy import Column, Integer, String
from app.database import Base

class Impact(Base):
    __tablename__ = "impacts"

    id = Column(Integer, primary_key=True, index=True)
    figures = Column(String(512), nullable=False)
    description = Column(String(512), nullable=False)
    category = Column(String(512), nullable=False)
