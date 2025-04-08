import asyncio
from fastapi import FastAPI
from app.routes import products, blogs, auth, instafeeds, clients, impacts, contacts, galleries
from app.database import engine, Base, create_tables, get_db
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import Limiter
from fastapi.responses import JSONResponse
from app.models.user import User
from app.utils.security import get_password_hash
from app.config import settings
from sqlalchemy.future import select

# 🚀 Ensure models are imported so SQLAlchemy registers them
from app.models import blog, product, user, instafeed, client, impact,contact, gallery # 👈 Critical fix for missing tables

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, please slow down!"}
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# 📌 Include API Routes
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(blogs.router)
app.include_router(instafeeds.router)
app.include_router(clients.router)
app.include_router(impacts.router)
app.include_router(contacts.router)
app.include_router(galleries.router)



# ✅ Function to create the admin user at startup
async def create_admin_user():
    async for session in get_db():  # Properly fetch DB session
        try:
            # Check if admin already exists
            result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
            admin = result.scalar_one_or_none()
            
            if not admin:
                password_hash = get_password_hash(settings.ADMIN_PASSWORD)
                admin_user = User(
                    username=settings.ADMIN_USERNAME,
                    email=settings.ADMIN_EMAIL,
                    hashed_password=password_hash,
                    is_admin=True
                )
                session.add(admin_user)
                await session.commit()
                print("✅ Admin user created")
            else:
                print("✅ Admin user already exists")

        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
        finally:
            await session.close()


@app.on_event("startup")
async def startup():
    print("🔄 Checking & creating database tables...")
    await create_tables()  # Should now work since models are imported
    await create_admin_user()

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}
