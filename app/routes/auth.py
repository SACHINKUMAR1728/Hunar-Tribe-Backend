from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from datetime import timedelta
from app.models.user import User
from app.schemas.user import UserInDB
from app.utils.security import verify_password, create_access_token

router = APIRouter()

@router.post("/auth/token", tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(hours=1)
    
    access_token = create_access_token(data = {"sub": user.email, "is_admin": user.is_admin}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
