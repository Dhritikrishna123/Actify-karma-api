# API settings and configuration


from pydantic import Field, BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Actify Karma System"
    DEBUG: bool = Field(default=os.getenv("DEBUG", "False").lower() == "true")
    
    # MongoDB Settings
    MONGODB_URL: str = Field(default=os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    MONGODB_DB: str = Field(default=os.getenv("MONGODB_DB", "actify_karma"))
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Export settings instance
__all__ = ["settings"]
