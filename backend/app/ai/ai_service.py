import asyncio
import httpx
from typing import Optional
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from app.core.config import settings
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = GigaChat(
            credentials=settings.GIGACHAT_CREDENTIALS.get_secret_value(),
            verify_ssl_certs=settings.GIGACHAT_VERIFY_SSL
        )

    def explain_topic(self, topic: str, grade: str = "8 класс") -> str:
        # Валидация
        if not topic.strip():
            raise ValueError("Topic cannot be empty")
        if len(topic) > 500:
            raise ValueError("Topic is too long (max 500 chars)")

        prompt = (
            f"Ты — дружелюбный репетитор по школьной программе РФ. "
            f"Объясни тему '{topic}' понятно, кратко и с примерами, "
            f"как будто ученик учится в {grade}. "
            f"Не используй сложные термины без пояснения. "
            f"Ответ дай в формате Markdown."
        )

        messages = [
            Messages(role=MessagesRole.SYSTEM, content="Ты — эксперт в школьном образовании."),
            Messages(role=MessagesRole.USER, content=prompt)
        ]

        chat = Chat(
            messages=messages,
            max_tokens=settings.GIGACHAT_MAX_TOKENS,
            temperature=settings.GIGACHAT_TEMPERATURE,
            top_p=settings.GIGACHAT_TOP_P
        )

        try:
            response = self.client.chat(chat)
            if not response.choices:
                raise HTTPException(status_code=500, detail="Empty response from AI")
            content = response.choices[0].message.content
            if not content:
                raise HTTPException(status_code=500, detail="No content in AI response")
            return content

        except httpx.TimeoutException:
            logger.error("GigaChat timeout")
            raise HTTPException(status_code=504, detail="AI service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"GigaChat HTTP error: {e}")
            raise HTTPException(status_code=502, detail="AI service error")
        except Exception as e:
            logger.error(f"Unexpected error in AI service: {e}")
            raise HTTPException(status_code=500, detail="Internal AI error")

    # async def close(self):
    #     """Вызвать при завершении приложения"""
    #     if self.client:
    #         await self.client.aclose()