from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,                     # Управляем через .env
    pool_size=settings.DB_POOL_SIZE,           # Например, 20
    max_overflow=settings.DB_MAX_OVERFLOW,     # Например, 20
    pool_recycle=3600,                         # Пересоздавать соединения каждые 1 час
    pool_pre_ping=True,                        # Проверять соединение перед использованием
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
