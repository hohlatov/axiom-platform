from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import api_router
from app.db.base import Base, engine
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Инициализация базы данных...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных инициализирована.")
    except Exception as e:
        logger.critical(f"Не удалось подключиться к базе данных: {e}")
        raise
    yield
    

app = FastAPI(title="AXIOM Platform", lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")
