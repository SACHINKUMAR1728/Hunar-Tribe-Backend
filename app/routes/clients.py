from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_admin
from app.schemas.client import ClientCreate, ClientUpdate, ClientInDB  # Assuming these exist
from app.models.client import Client
from slowapi import Limiter
from slowapi.util import get_remote_address



limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/clients", response_model=list[ClientInDB], tags=["clients"])
@limiter.limit("100/minute")
async def read_clients(
    request: Request,  # Added to support SlowAPI rate limiter
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Client).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/clients/{client_id}", response_model=ClientInDB, tags=["clients"])
async def read_client(client_id: int, db: AsyncSession = Depends(get_db)):
    client = await db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/admin/clients", response_model=ClientInDB, tags=["clients"])
async def create_client(
    client: ClientCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client

@router.put("/admin/clients/{client_id}", response_model=ClientInDB, tags=["clients"])
async def update_client(
    client_id: int,
    client: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_client = await db.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)
    
    await db.commit()
    await db.refresh(db_client)
    return db_client

@router.delete("/admin/clients/{client_id}", response_model=ClientInDB, tags=["clients"])
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    db_client = await db.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await db.delete(db_client)
    await db.commit()
    return db_client
