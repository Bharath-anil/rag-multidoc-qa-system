from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    MODEL_NAME: str = "all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"

settings = Settings()