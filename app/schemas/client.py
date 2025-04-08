from pydantic import BaseModel
from typing import Optional
from pydantic import ConfigDict


class ClientBase(BaseModel):
    name: str
    logo_url: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None

class Client(ClientBase):
    id: int

class ClientInDB(Client):
    model_config = ConfigDict(from_attributes=True)  # Correct for Pydantic V2