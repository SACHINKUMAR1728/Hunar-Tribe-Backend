from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_admin
from app.schemas.instafeed import InstaFeedCreate, InstaFeedUpdate, InstaFeedInDB # Assuming these exist
from app.models.instafeed import InstaFeed
from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/instafeeds", response_model=list[InstaFeedInDB], tags=["instafeeds"])
@limiter.limit("100/minute")
async def read_instafeeds(
    request: Request,  # Added to support SlowAPI rate limiter
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(InstaFeed).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/instafeeds/{instafeed_id}", response_model=InstaFeedInDB, tags=["instafeeds"])
async def read_instafeed(instafeed_id: int, db: AsyncSession = Depends(get_db)):
    instafeed = await db.get(InstaFeed, instafeed_id)
    if not instafeed:
        raise HTTPException(status_code=404, detail="InstaFeed not found")
    return instafeed

@router.post("/admin/instafeeds", response_model=InstaFeedInDB, tags=["instafeeds"])
async def create_instafeed(
    instafeed: InstaFeedCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_instafeed = InstaFeed(**instafeed.model_dump(), author_id=admin.id)  # Fixed dict() -> model_dump()
    db.add(db_instafeed)
    await db.commit()
    await db.refresh(db_instafeed)
    return db_instafeed

@router.put("/admin/instafeeds/{instafeed_id}", response_model=InstaFeedInDB, tags=["instafeeds"])
async def update_instafeed(
    instafeed_id: int,
    instafeed: InstaFeedUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_instafeed = await db.get(InstaFeed, instafeed_id)
    if not db_instafeed:
        raise HTTPException(status_code=404, detail="InstaFeed not found")
    
    for key, value in instafeed.model_dump(exclude_unset=True).items():
        setattr(db_instafeed, key, value)
    
    await db.commit()
    await db.refresh(db_instafeed)
    return db_instafeed

@router.delete("/admin/instafeeds/{instafeed_id}", response_model=InstaFeedInDB, tags=["instafeeds"])
async def delete_instafeed(
    instafeed_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_instafeed = await db.get(InstaFeed, instafeed_id)
    if not db_instafeed:
        raise HTTPException(status_code=404, detail="InstaFeed not found")
    
    await db.delete(db_instafeed)
    await db.commit()
    return {"message": "InstaFeed deleted successfully"}

