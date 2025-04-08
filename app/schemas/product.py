from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    image_url: str
    description: Optional[str] = None
    swiggy_mart_link: str
    price: str
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    image_url: str
    description: Optional[str] = None
    swiggy_mart_link: str
    price: Optional[str] = None
    is_active: Optional[bool] = None

class ProductInDB(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2
