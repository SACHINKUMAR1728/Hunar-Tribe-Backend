from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # ⚠ This should be hashed before storing in the DB

class UserInDB(UserBase):
    id: int
    is_admin: bool
    hashed_password: str  # ✅ Secure storage instead of plain password

    model_config = ConfigDict(from_attributes=True)  # ✅ Pydantic V2 compatible
    
class UserResponse(UserBase):
    id: int
    is_admin: bool
