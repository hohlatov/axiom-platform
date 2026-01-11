from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя, будет использован для входа")
    password: str = Field(..., min_length=8, max_length=128, description="Пароль от 8 до 128 символов")
    full_name: str = Field(..., max_length=100, description="Полное имя пользователя")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Literal["student", "teacher", "admin"]  # Жёстко заданные значения

    class Config:
        from_attributes = True