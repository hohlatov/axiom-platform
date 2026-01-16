from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, SecretStr, Field, ConfigDict
import os
from pprint import pprint

class Settings(BaseSettings):
    #  Безопасность / JWT
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # База данных
    DATABASE_URL: str
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 20
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_TTL_SECONDS: int = 3600
        
    # Внешние сервисы
    GIGACHAT_CREDENTIALS: SecretStr
    GIGACHAT_VERIFY_SSL: bool = False
    GIGACHAT_MODEL: str = "GigaChat"
    GIGACHAT_MAX_TOKENS: int = 1000
    GIGACHAT_TEMPERATURE: float = 0.7
    GIGACHAT_TOP_P: float = 0.9

    model_config = ConfigDict(env_file=".env")
    
settings = Settings()