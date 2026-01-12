"""
Database import/export endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Updated: 2025-12-05 - Removed PDF import, sample data, and database management functions
Updated: 2025-12-05 - Fixed database import to properly reload database connections
"""

# 已修改於 2025-12-05，原因：移除 PDF 匯入、範例資料和資料庫管理功能，僅保留資料庫匯出/匯入
# 已修改於 2025-12-05，原因：新增資料庫連接重載功能以修正匯入後資料未更新的問題
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import shutil
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

router = APIRouter(prefix="", tags=["Import"])

# 已新增於 2025-01-12，原因：設定資料庫匯入的檔案大小限制為 100MB
MAX_DB_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# 已移除於 2025-12-05，原因：移除 PDF 匯入功能
# 原函式：import_pdf - 上傳 PDF 並匯入履歷資料

# 已移除於 2025-12-05，原因：移除範例履歷資料匯入功能
# 原函式：import_resume_data - 匯入範例履歷資料

# 已移除於 2025-12-05，原因：移除資料庫管理功能
# 原函式：create_database - 重新建立資料庫表格


# 已新增於 2025-11-30，原因：新增資料庫匯出功能以方便遷移主機
# 已修正於 2025-12-01，原因：修正路徑解析以正確定位資料庫檔案，與 config.py 中 DATABASE_URL 一致
# 已修正於 2025-12-05，原因：修正路徑錯誤，DATABASE_URL 相對於 backend 目錄而非專案根目錄
@router.get("/database/export/")
async def export_database():
    """
    Export the SQLite database file for backup or migration
    """
    try:
        # 已修正於 2025-12-05，原因：DATABASE_URL = "sqlite:///./data/resume.db" 相對於 backend 目錄
        # 原錯誤：使用 project_root (ResumexLab) -> 導致路徑為 ResumexLab/data/resume.db
        # 正確：使用 backend_dir -> 路徑為 ResumexLab/backend/data/resume.db
        # 從 backend/app/api/endpoints/import_data.py 向上 4 層到 backend 目錄
        backend_dir = Path(__file__).parent.parent.parent.parent.resolve()
        db_path = backend_dir / "data" / "resume.db"

        # Verify the database file exists
        if not db_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Database file not found at {db_path}"
            )

        # Create a timestamped filename for the export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"resume_db_backup_{timestamp}.db"

        # Return the database file as a download
        return FileResponse(
            path=str(db_path),
            media_type="application/octet-stream",
            filename=export_filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting database: {str(e)}"
        )


# 已新增於 2025-11-30，原因：新增資料庫匯入功能以方便遷移主機
# 已修正於 2025-12-01，原因：修正路徑解析以正確定位資料庫檔案，與 config.py 中 DATABASE_URL 一致
# 已修正於 2025-12-05，原因：新增資料庫連接重載機制，修正匯入後資料未更新的問題
# 已修正於 2025-12-05，原因：修正路徑錯誤，使用正確的 backend/data/resume.db 路徑
@router.post("/database/import/")
async def import_database(file: UploadFile = File(...)):
    """
    Import a SQLite database file (for restoration or migration)
    WARNING: This will replace the current database!

    已修改於 2025-01-12，原因：新增檔案大小檢查，限制為 100MB
    """
    if not file.filename.lower().endswith('.db'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .db files are allowed"
        )

    # 已新增於 2025-01-12，原因：檢查檔案大小
    # 讀取檔案內容以檢查大小
    file_content = await file.read()
    file_size = len(file_content)

    if file_size > MAX_DB_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_DB_FILE_SIZE / (1024 * 1024):.0f}MB"
        )

    # 重置檔案指標以便後續讀取
    await file.seek(0)

    try:
        # 已修正於 2025-12-05，原因：DATABASE_URL = "sqlite:///./data/resume.db" 相對於 backend 目錄
        # 原錯誤：使用 project_root (ResumexLab) -> 導致路徑為 ResumexLab/data/resume.db
        # 正確：使用 backend_dir -> 路徑為 ResumexLab/backend/data/resume.db
        # 從 backend/app/api/endpoints/import_data.py 向上 4 層到 backend 目錄
        backend_dir = Path(__file__).parent.parent.parent.parent.resolve()
        db_path = backend_dir / "data" / "resume.db"

        # 確保 data 目錄存在
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a backup of the current database if it exists
        backup_created = False
        if db_path.exists():
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backend_dir / "data" / f"resume_backup_{backup_timestamp}.db"
            shutil.copy2(db_path, backup_path)
            backup_created = True

        # 已新增於 2025-12-05，原因：在覆寫資料庫前，先關閉所有現有連接
        # Step 1: Close all existing database connections
        from app.db.base import engine, SessionLocal

        # Dispose of the current engine (closes all connections in the pool)
        engine.dispose()

        # 已修改於 2025-01-12，原因：使用已讀取的檔案內容直接寫入
        # Save the uploaded database file
        with open(db_path, "wb") as buffer:
            buffer.write(file_content)

        # 已新增於 2025-12-05，原因：資料庫檔案更新後，重新建立資料庫引擎和 Session
        # Step 2: Recreate the engine and SessionLocal with the new database file
        from app.core.config import settings
        import app.db.base as db_base

        # Create new engine
        new_engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}
        )

        # Replace the global engine and SessionLocal
        db_base.engine = new_engine
        db_base.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=new_engine)

        # Verify the new database can be accessed
        test_session = db_base.SessionLocal()
        try:
            # Try a simple query to verify the database is accessible
            # 已修正於 2025-12-05，原因：SQLAlchemy 2.0 要求使用 text() 函數執行原始 SQL
            test_session.execute(text("SELECT 1"))
            test_session.close()
        except Exception as verify_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Imported database file is not valid: {str(verify_error)}"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Database imported successfully. Database connections have been reloaded.",
                "filename": file.filename,
                "backup_created": backup_created
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing database: {str(e)}"
        )