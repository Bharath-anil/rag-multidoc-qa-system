from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    DATABASE_URL: str
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    SECRET_KEY: str
    class Config:
        env_file = ".env"

settings = Settings()