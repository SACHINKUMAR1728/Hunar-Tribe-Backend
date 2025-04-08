from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_admin
from app.schemas.impact import ImpactCreate, ImpactUpdate, ImpactInDB  # Assuming these exist
from app.models.impact import Impact
from slowapi import Limiter
from slowapi.util import get_remote_address




limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/impacts", response_model=list[ImpactInDB], tags=["impacts"])
@limiter.limit("100/minute")
async def read_impacts(
    request: Request,  # Added to support SlowAPI rate limiter
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Impact).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/impacts/{impact_id}", response_model=ImpactInDB, tags=["impacts"])
async def read_impact(impact_id: int, db: AsyncSession = Depends(get_db)):
    impact = await db.get(Impact, impact_id)
    if not impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    return impact

@router.post("/admin/impacts", response_model=ImpactInDB, tags=["impacts"])
async def create_impact(
    impact: ImpactCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_impact = Impact(**impact.model_dump())
    db.add(db_impact)
    await db.commit()
    await db.refresh(db_impact)
    return db_impact

@router.put("/admin/impacts/{impact_id}", response_model=ImpactInDB, tags=["impacts"])
async def update_impact(
    impact_id: int,
    impact: ImpactUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_impact = await db.get(Impact, impact_id)
    if not db_impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    
    for key, value in impact.model_dump(exclude_unset=True).items():
        setattr(db_impact, key, value)
    
    await db.commit()
    await db.refresh(db_impact)
    return db_impact

@router.delete("/admin/impacts/{impact_id}", response_model=ImpactInDB, tags=["impacts"])
async def delete_impact(
    impact_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_impact = await db.get(Impact, impact_id)
    if not db_impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    
    await db.delete(db_impact)
    await db.commit()
    return db_impact
