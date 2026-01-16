from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.api.v1.dependencies import get_ai_service
from app.ai.ai_service import AIService
from app.db.base import get_db

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    ai_service: AIService = Depends(get_ai_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Получает тему от ученика → ИИ объясняет понятно.
    """
    
    reply = await ai_service.explain_topic(request.message, grade="8 класс", db=db)
    return ChatResponse(reply=reply)