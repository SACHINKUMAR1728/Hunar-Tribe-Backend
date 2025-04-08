from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.dependencies import get_current_admin
from app.models.user import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

# Public: Get list of products
@router.get("/products", tags=["products"], response_model=list[ProductInDB])
@limiter.limit("100/minute")
async def read_products(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(Product).where(Product.is_deleted == False).offset(skip).limit(limit))
    return results.scalars().all()

# Public: Get product by ID
@router.get("/products/{id}", tags=["products"], response_model=ProductInDB)
async def read_product(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == id, Product.is_deleted == False))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Admin: Create a new product
@router.post("/admin/products", response_model=ProductInDB, tags=["products"])
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_product = Product(**product.model_dump())  # Corrected from dict() to model_dump()
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Admin: Update product by ID
@router.put("/admin/products/{id}", response_model=ProductInDB, tags=["products"])
async def update_product(
    id: int,
    product_update: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    result = await db.execute(select(Product).where(Product.id == id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_update.model_dump(exclude_unset=True).items():  # Corrected from dict() to model_dump()
        setattr(db_product, key, value)
    
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Admin: Soft delete product by ID
@router.delete("/admin/products/{id}", tags=["products"])
async def delete_product(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(Product).where(Product.id == id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.is_deleted = True  # Assuming soft delete is implemented
    await db.commit()
    return {"message": "Product deleted successfully"}
