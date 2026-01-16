from fastapi import Depends
from app.ai.ai_service import AIService

def get_ai_service() -> AIService:
    return AIService()