from sqlalchemy import Column, Integer, String
from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    logo_url = Column(String(512), nullable=False)
    