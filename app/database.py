import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Enable SQLAlchemy Debug Logging
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Define Base Model
Base = declarative_base()

# Database Connection URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Create Async Engine 
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Create Async Session
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency for FastAPI Routes
async def get_db():
    async with async_session() as session:
        yield session


# ✅ Function to Manually Create Tables (Run in `main.py`)
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise