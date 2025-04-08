from pydantic import BaseModel, ConfigDict
from typing import Optional
 


class GalleryBase(BaseModel):
    title: str
    description: str
    image_url: str
    
class GalleryCreate(GalleryBase):
    pass    

class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

class Gallery(GalleryBase):
    id: int

class GalleryInDB(Gallery):
    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2