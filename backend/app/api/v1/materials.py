from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.models.user import User
from app.schemas.material import MaterialCreate, MaterialResponse
from app.crud.material import create_material, get_materials
from app.api.v1.auth import get_current_user
from app.models.material import Material

router = APIRouter(prefix="/materials", tags=["materials"])

@router.post("/", response_model=MaterialResponse)
async def create_material_endpoint(
    material: MaterialCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_material = Material(**material.model_dump())
    return await create_material(db, db_material, owner_id=current_user.id)

@router.get("/", response_model=list[MaterialResponse])
async def read_materials(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await get_materials(db, skip=skip, limit=limit)
