from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareIN AI Call Summary"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:Dsouza5451@127.0.0.1:5432/aicallsummary"

    GEMINI_API_KEY: str = "AIzaSyC1-3Ecw-U23q0OAxchPgwrEt0lMroTWfI"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()