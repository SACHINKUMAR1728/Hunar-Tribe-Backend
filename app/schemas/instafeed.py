from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict
from datetime import datetime

class InstaFeedBase(BaseModel):
    post_id: str

class InstaFeedCreate(InstaFeedBase):
    pass

class InstaFeedUpdate(BaseModel):
    post_id: str

class InstaFeed(InstaFeedBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None  # Already optional

class InstaFeedInDB(InstaFeed):
    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2
