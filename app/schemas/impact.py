from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict
from datetime import datetime

class ImpactBase(BaseModel):
    figures: str
    description: str
    category: str

class ImpactCreate(ImpactBase):
    pass

class ImpactUpdate(BaseModel):
    figures: str
    description: str
    category: str

class Impact(ImpactBase):
    id: int

class ImpactInDB(Impact):
    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2

