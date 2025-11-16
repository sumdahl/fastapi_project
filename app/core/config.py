from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    ENV: str = "development"
    DATABASE_URL: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
