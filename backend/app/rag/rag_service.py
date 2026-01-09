from openai import AsyncOpenAI
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def explain(self, topic: str, grade: str = "8 класс") -> str:
        prompt = f"""
        Ты — дружелюбный репетитор по школьной программе.
        Объясни тему '{topic}' понятно, кратко и с примерами, как будто ученик учится в {grade}.
        Не используй сложные термины без пояснения.
        """
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content