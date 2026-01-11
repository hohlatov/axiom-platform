from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.ai.ai_service import AIService
import logging

router = APIRouter(prefix="/ai", tags=["AI Репетитор"])

# Инициализация сервиса (лучше — через зависимость, а не глобально)
ai_service = AIService()

logger = logging.getLogger(__name__)

class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300, description="Тема для объяснения")
    grade: str = Field("8 класс", max_length=50, description="Класс или уровень ученика")

@router.post("/explain")
def explain_topic(request: ExplainRequest):
    try:
        explanation = ai_service.explain_topic(request.topic, request.grade)
        return {"explanation": explanation}
    except HTTPException:
        # Пробрасываем HTTP-исключения напрямую
        raise
    except Exception as e:
        logger.error(f"Ошибка в AI-сервисе: {e}", exc_info=True)  # Без эмодзи
        raise HTTPException(status_code=500, detail="Ошибка при генерации объяснения")