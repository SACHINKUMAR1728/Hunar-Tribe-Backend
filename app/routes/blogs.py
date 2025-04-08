from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate, BlogInDB  # Assuming BlogInDB exists
from app.dependencies import get_current_admin
from app.models.user import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

# Public: Get all blogs
@router.get("/blogs", response_model=list[BlogInDB], tags=["blogs"])
@limiter.limit("100/minute")
async def read_blogs(
    request: Request,  # Added to support SlowAPI rate limiter
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Blog).offset(skip).limit(limit))
    return result.scalars().all()

# Public: Get a specific blog by ID
@router.get("/blogs/{blog_id}", response_model=BlogInDB, tags=["blogs"])
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# Admin: Create a new blog
@router.post("/admin/blogs", response_model=BlogInDB, tags=["blogs"])
async def create_blog(
    blog: BlogCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_blog = Blog(**blog.model_dump(), author_id=admin.id)  # Fixed dict() -> model_dump()
    db.add(db_blog)
    await db.commit()
    await db.refresh(db_blog)
    return db_blog

# Admin: Update a blog by ID
@router.put("/admin/blogs/{blog_id}", response_model=BlogInDB, tags=["blogs"])
async def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_blog = await db.get(Blog, blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    for key, value in blog.model_dump(exclude_unset=True).items():  # Fixed dict() -> model_dump()
        setattr(db_blog, key, value)
    
    await db.commit()
    await db.refresh(db_blog)
    return db_blog

# Admin: Delete a blog by ID
@router.delete("/admin/blogs/{blog_id}", tags=["blogs"])
async def delete_blog(
    blog_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    blog = await db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    await db.delete(blog)
    await db.commit()
    return {"message": "Blog deleted successfully"}
