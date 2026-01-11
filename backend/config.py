"""
Configuration management for the application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "chatbot_db"
    
    # AI
    GEMINI_API_KEY: str = ""
    
    # Backend
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Excel Data
    EXCEL_FILE_PATH: str = "../Banking Demo File.xlsx"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
