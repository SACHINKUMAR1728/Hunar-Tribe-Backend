from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.utils.security import verify_token
from app.schemas.user import UserInDB
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/token")

async def get_current_admin(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        print(f"Decoded payload: {payload}")  # Debugging line to check the payload
        if not payload or "sub" not in payload or "is_admin" not in payload:
            raise credentials_exception

        if not payload["is_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        # ✅ Fetch the full user details from DB
        result = await db.execute(select(User).where(User.email == payload["sub"]))
        user = result.scalar_one_or_none()

        if not user:
            raise credentials_exception

        return UserInDB(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            hashed_password=user.hashed_password
        )
    except Exception as e:
        raise credentials_exception
