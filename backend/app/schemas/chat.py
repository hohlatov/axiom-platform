from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Запрос на объяснение темы от пользователя.
    """
    message: str
    
class ChatResponse(BaseModel):
    """
    Ответ ИИ на запрос пользователя.
    """
    reply: str