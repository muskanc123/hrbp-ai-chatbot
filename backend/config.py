"""
Configuration management for the application
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "chatbot_db"
    
    # AI
    GEMINI_API_KEY: str = ""
    
    # Backend
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Excel Data
    EXCEL_FILE_PATH: str = "../Banking Demo File.xlsx"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
