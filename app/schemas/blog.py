from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BlogBase(BaseModel):
    title: str
    content: str
    featured_image_url: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    featured_image_url: Optional[str] = None

class Blog(BlogBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None  # Already optional

class BlogInDB(Blog):
    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2
