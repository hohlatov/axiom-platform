from fastapi import APIRouter
from .auth import router as auth_router
from .ai import router as ai_router 

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(ai_router) 