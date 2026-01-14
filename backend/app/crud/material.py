from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.material import Material

async def create_material(db: AsyncSession, material: Material, owner_id: int):
    material.owner_id = owner_id
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return material

async def get_materials(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Material).offset(skip).limit(limit))
    return result.scalars().all()