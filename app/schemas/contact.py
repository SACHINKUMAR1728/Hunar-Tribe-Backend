from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    email: str
    phone_number: str
    message: str

class ContactCreate(ContactBase):
    pass


class ContactInDB(ContactBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2