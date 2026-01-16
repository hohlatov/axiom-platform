import asyncio
import httpx
from typing import Optional
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from app.core.config import settings
from app.db.redis import cache
from app.ai.embedding import TextEmbedder
from app.models.material import Material
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import asyncio
import logging
import hashlib
import numpy as np

logger = logging.getLogger(__name__)

def _make_cache_key(topic: str, grade: str) -> str:
    """Создаёт уникальный ключ на основе темы и класса"""
    key = f"explain:{topic}:{grade}".lower()
    return hashlib.md5(key.encode()).hexdigest()

class AIService:
    def __init__(self):
        self.client = GigaChat(
            credentials=settings.GIGACHAT_CREDENTIALS.get_secret_value(),
            verify_ssl_certs=settings.GIGACHAT_VERIFY_SSL
        )
        self.embedder = TextEmbedder()
        self.material_cache = None
        
    async def _get_all_materials(self, db: AsyncSession) -> list[Material]:
        if not self.material_cache:
            result = await db.execute(select(Material))
            self.material_cache = result.scalars().all()
        return self.material_cache
    
    async def _find_relevant_material(self, query: str, db: AsyncSession, top_k: int = 1) -> list[Material]:
        materials = await self._get_all_materials(db)
        if not materials:
            return []
        
        # Кодируем запрос
        query_emb = self.embedder.encode([query])[0]
        material_embs = self.embedder.encode([m.title + ". " + m.content for m in materials])
        
        # Считаем схожесть
        similarities = [
            self.embedder.consine_similarity(query_emb, mat_emb)
            for mat_emb in material_embs
        ]
        
        # Возвращаем топ-К
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [materials[i] for i in top_indices if similarities[i] > 0.5]

    async def explain_topic(self, topic: str, grade: str = "8 класс", db: AsyncSession = None) -> str:
        if not db:
            raise ValueError("DB session required for RAG")
        
        cache_key = _make_cache_key(topic, grade)
        cached = await cache.get(cache_key)
        if cached:
            return cached
        
        # Ищем релевантные материалы
        relevant_materials = await self._find_relevant_material(topic, db)
        
        if relevant_materials:
            context = "\n\n".join([
                f"Материал: {m.title}\n{m.content}" for m in relevant_materials
            ])
            prompt = (
                f"На основе следующих материалов объясни тему '{topic}' просто и понятно, "
                f"как ученику {grade}. Сохрани стиль и терминологию.\n\n"
                f"{context}"
            )
        else:
            prompt = (
                f"Ты — дружелюбный репетитор. Объясни тему '{topic}' понятно и с примерами, "
                f"как ученику {grade}. Ответ в Markdown."
            )
            
        messages = [
            Messages(role=MessagesRole.SYSTEM, content="Ты - эксперт в школьном образовании."),
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
            content = response.choices[0].message.content
            if not content:
                raise HTTPException(status_code=500, detail="No content in AI response")
            
            await cache.set(cache_key, content)
            return content
        
        except Exception as e:
            logger.error(f"AI error: {e}")
            raise HTTPException(status_code=500, detail="Internal AI error")
        
        # Валидация
        if not topic.strip():
            raise ValueError("Topic cannot be empty")
        if len(topic) > 500:
            raise ValueError("Topic is too long (max 500 chars)")
        
        cache_key = _make_cache_key(topic, grade)
        cashed = await cache.get(cache_key)
        if cashed:
            return cashed
        
        # Если нет - обращаемся к GigaChat
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