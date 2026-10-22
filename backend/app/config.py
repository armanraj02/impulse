from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ANALYTICS_DB_HOST: str = "localhost"
    ANALYTICS_DB_PORT: str = "5432"
    ANALYTICS_DB_NAME: str = "academic_analytics_db"
    ANALYTICS_DB_USER: str = "analytics_readonly"
    ANALYTICS_DB_PASSWORD: str = "readonly123"
    
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
