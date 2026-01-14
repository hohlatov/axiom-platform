from fastapi import APIRouter
from .auth import router as auth_router
from .ai import router as ai_router 
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.materials import router as materials_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/auth", tags=["users"])
api_router.include_router(materials_router, prefix="", tags=["materials"])
api_router.include_router(ai_router) 