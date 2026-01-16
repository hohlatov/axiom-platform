import asyncio
from app.core.config import settings
from app.ai.ai_service import AIService

async def test():
    service = AIService()
    try:
        result = await service.explain_topic("Что такое дробь?", "5 класс")
        print("✅ Успех:")
        print(result)
    except Exception as e:
        print("❌ Ошибка:")
        print(e)

if __name__ == "__main__":
    asyncio.run(test())