from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactInDB
from app.dependencies import get_current_admin
from app.models.user import User


limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.get("/admin/contacts", tags=["contacts"], response_model=list[ContactInDB])
@limiter.limit("100/minute")
async def read_contacts(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)):
    results = await db.execute(select(Contact).offset(skip).limit(limit))

    return results.scalars().all()

@router.get("/admin/contacts/{id}", tags=["contacts"], response_model=ContactInDB)
async def read_contact(id: int, db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)):
    result = await db.execute(select(Contact).where(Contact.id == id))
    contact = result.scalars().first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/contacts", response_model=ContactInDB, tags=["contacts"])
async def create_contact(
    contact: ContactCreate,
    db: AsyncSession = Depends(get_db),
    
):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

@router.delete("/admin/contacts/{id}", tags=["contacts"])
async def delete_contact(id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(Contact).where(Contact.id == id))
    db_contact = result.scalars().first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    await db.delete(db_contact)
    await db.commit()
    return {"detail": "Contact deleted successfully"}