from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.models.gallery import Gallery
from app.schemas.gallery import GalleryCreate, GalleryUpdate, GalleryInDB  # Assuming GalleryInDB exists
from app.dependencies import get_current_admin
from app.models.user import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/galleries", response_model=list[GalleryInDB], tags=["galleries"])
@limiter.limit("100/minute")
async def read_galleries(
    request: Request,  # Added to support SlowAPI rate limiter
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Gallery).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/galleries/{gallery_id}", response_model=GalleryInDB, tags=["galleries"])
async def read_gallery(gallery_id: int, db: AsyncSession = Depends(get_db)):
    gallery = await db.get(Gallery, gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return gallery

@router.post("/admin/galleries", response_model=GalleryInDB, tags=["galleries"])
async def create_gallery(
    gallery: GalleryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_gallery = Gallery(**gallery.model_dump())
    db.add(db_gallery)
    await db.commit()
    await db.refresh(db_gallery)
    return db_gallery

@router.put("/admin/galleries/{gallery_id}", response_model=GalleryInDB, tags=["galleries"])
async def update_gallery(
    gallery_id: int,
    gallery: GalleryUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_gallery = await db.get(Gallery, gallery_id)
    if not db_gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    
    for key, value in gallery.model_dump(exclude_unset=True).items():
        setattr(db_gallery, key, value)
    
    await db.commit()
    await db.refresh(db_gallery)
    return db_gallery

@router.delete("/admin/galleries/{gallery_id}", tags=["galleries"])
async def delete_gallery(
    gallery_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_gallery = await db.get(Gallery, gallery_id)
    if not db_gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    
    await db.delete(db_gallery)
    await db.commit()
    return {"detail": "Gallery deleted successfully"}