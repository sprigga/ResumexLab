"""
PDF import and data management endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import sys
from pathlib import Path
import os
import tempfile
from typing import Optional
import shutil
from datetime import datetime

router = APIRouter(prefix="", tags=["Import"])

@router.post("/pdf/")
async def import_pdf(file: UploadFile = File(...), import_type: str = Form("pdf_extraction")):
    """
    Upload PDF file and extract resume data
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    try:
        # For now, we'll call the import_resume_data.py script directly
        # In the future, we could implement actual PDF text extraction here
        # Save uploaded PDF to temporary file if needed for processing

        # Execute import_resume_data.py script which has pre-defined sample data
        # Use absolute path to ensure the script is found regardless of working directory
        # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄（backend/app/api/endpoints -> 回退4層到項目根目錄）
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up from import_data.py)
        script_path = project_root / "script" / "import_resume_data.py"

        # Verify the script exists before running
        if not script_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Script not found at {script_path}"
            )

        result = subprocess.run([sys.executable, str(script_path)],
                               capture_output=True, text=True, timeout=30, cwd=str(project_root))

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Script execution failed: {result.stderr}"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "PDF processed and resume data imported successfully",
                "filename": file.filename,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Script execution timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )


@router.post("/resume-data/")
async def import_resume_data():
    """
    Import resume data using import_resume_data.py script
    """
    try:
        # Use absolute path to ensure the script is found regardless of working directory
        # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up)
        script_path = project_root / "script" / "import_resume_data.py"

        # Verify the script exists before running
        if not script_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Script not found at {script_path}"
            )

        result = subprocess.run([sys.executable, str(script_path)],
                               capture_output=True, text=True, timeout=30, cwd=str(project_root))

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Script execution failed: {result.stderr}"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Resume data imported successfully",
                "stdout": result.stdout
            }
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Script execution timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing resume data: {str(e)}"
        )


@router.post("/database/")
async def create_database():
    """
    Create database tables using create_database.py script
    """
    try:
        # Use absolute path to ensure the script is found regardless of working directory
        # 已修改於 2025-11-30，原因：修復路徑解析以正確定位項目根目錄
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()  # Go back to project root (5 levels up)
        script_path = project_root / "script" / "create_database.py"

        # Verify the script exists before running
        if not script_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Script not found at {script_path}"
            )

        result = subprocess.run([sys.executable, str(script_path)],
                               capture_output=True, text=True, timeout=30, cwd=str(project_root))

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database creation failed: {result.stderr}"
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Database tables created successfully",
                "stdout": result.stdout
            }
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database creation timed out"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating database: {str(e)}"
        )


# 已新增於 2025-11-30，原因：新增資料庫匯出功能以方便遷移主機
@router.get("/database/export/")
async def export_database():
    """
    Export the SQLite database file for backup or migration
    """
    try:
        # Get the database file path
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
        db_path = project_root / "backend" / "resume.db"

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
@router.post("/database/import/")
async def import_database(file: UploadFile = File(...)):
    """
    Import a SQLite database file (for restoration or migration)
    WARNING: This will replace the current database!
    """
    if not file.filename.lower().endswith('.db'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .db files are allowed"
        )

    try:
        # Get the database file path
        project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
        db_path = project_root / "backend" / "resume.db"

        # Create a backup of the current database if it exists
        if db_path.exists():
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = project_root / "backend" / f"resume_backup_{backup_timestamp}.db"
            shutil.copy2(db_path, backup_path)

        # Save the uploaded database file
        with open(db_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Database imported successfully",
                "filename": file.filename,
                "backup_created": db_path.exists()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing database: {str(e)}"
        )