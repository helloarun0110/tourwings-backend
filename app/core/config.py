# This file uses pydantic-settings for configuration
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    PROJECT_NAME: str = "Tour Booking API"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    # DATABASE_URL: str = "mysql+aiomysql://touruser:tourPass41!@localhost:3306/tourwings"
    ASYNC_DATABASE_URL: str
    SYNC_DATABASE_URL: str

    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
