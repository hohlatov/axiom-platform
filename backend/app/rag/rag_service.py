from gigachat import AsyncGigaChat
from gigachat.models import Chat, Messages, MessagesRole
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.client = AsyncGigaChat(
            credentials=settings.GIGACHAT_CREDENTIALS.get_secret_value(),
            verify_ssl_certs=settings.GIGACHAT_VERIFY_SSL
        )
        self.model = settings.GIGACHAT_MODEL  # например, "GigaChat"
        self.max_tokens = settings.GIGACHAT_MAX_TOKENS  # например, 1000
        self.temperature = settings.GIGACHAT_TEMPERATURE  # например, 0.7

    async def explain(self, topic: str, grade: str = "8 класс") -> str:
        # Валидация входа
        if not topic or len(topic.strip()) == 0:
            raise ValueError("Topic cannot be empty")
        if len(topic) > 300:
            raise ValueError("Topic is too long (max 300 chars)")

        prompt = (
            f"Ты — дружелюбный репетитор по школьной программе РФ.\n"
            f"Объясни тему '{topic}' понятно, кратко и с примерами, как будто ученик учится в {grade}.\n"
            f"Не используй сложные термины без пояснения.\n"
            f"Ответ дай в формате Markdown."
        )

        messages = [
            Messages(role=MessagesRole.SYSTEM, content="Ты — эксперт в школьном образовании."),
            Messages(role=MessagesRole.USER, content=prompt)
        ]

        chat = Chat(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        try:
            response = await self.client.achat(chat)

            if not response.choices:
                raise RuntimeError("Empty response from GigaChat")

            message = response.choices[0].message
            content = message.content if message.content else ""

            if not content.strip():
                raise RuntimeError("No content in GigaChat response")

            return content.strip()

        except Exception as e:
            logger.error(f"GigaChat API error: {e}", exc_info=True)
            raise RuntimeError("Не удалось получить объяснение. Повторите попытку позже.")