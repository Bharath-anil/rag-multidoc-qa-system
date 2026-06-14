from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    DATABASE_URL: str
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    SECRET_KEY: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str
    DELETE_RETENTION_DAYS :int= 10
    class Config:
        env_file = ".env"

settings = Settings()