from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    """Application settings"""

    # Project info
    PROJECT_NAME: str = "Resume Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database
    # 原本設定 (已註解於 2025-11-29，原因：統一資料庫路徑到 backend 目錄)
    # DATABASE_URL: str = "sqlite:///./resume.db"
    # 第二次修改設定 (已註解於 2025-11-30，原因：路徑錯誤，實際不存在 backend/backend/resume.db)
    # DATABASE_URL: str = "sqlite:///./backend/resume.db"
    # 新設定 (修改於 2025-11-30，原因：統一資料庫路徑到 data 目錄，配合 Docker volume 掛載)
    DATABASE_URL: str = "sqlite:///./data/resume.db"

    # Security
    # 原本硬編碼設定 (已註解於 2025-11-30，原因：修正 GitGuardian 安全警告，改用環境變數)
    # SECRET_KEY: str = "your-secret-key-change-this-in-production"
    # 新設定：從環境變數讀取，若無則自動生成（僅供開發使用）
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    # 原本設定 (已註解於 2025-11-30，原因：新增實際前端運行端口 5175)
    # BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    # 新設定：包含所有可能的前端端口（已更新於 2025-11-30，原因：修正容器端口為 58432）
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5175", "http://localhost:3000", "http://localhost:58432"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
