from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    HOST: str
    APP_NAME: str
    PORT: str
    APP_VERSION: str
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
    
    class Config:
        env_path = Path(__file__).parent.parent.parent / ".env"
        env_file = env_path
        env_file_encoding = "utf-8"


settings = Settings()
