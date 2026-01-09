from fastapi import FastAPI
from app.api.v1.endpoints import api_router
from app.db.base import Base, engine

app = FastAPI(title="AXIOM Platform")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix="/api/v1")
