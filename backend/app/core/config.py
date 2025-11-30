from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Project info
    PROJECT_NAME: str = "Resume Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database
    # 原本設定 (已註解於 2025-11-29，原因：統一資料庫路徑到 backend 目錄)
    # DATABASE_URL: str = "sqlite:///./resume.db"
    # 新設定：明確指定 backend 目錄下的資料庫
    DATABASE_URL: str = "sqlite:///./backend/resume.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    # 原本設定 (已註解於 2025-11-30，原因：新增實際前端運行端口 5175)
    # BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    # 新設定：包含所有可能的前端端口
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5175", "http://localhost:3000"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
