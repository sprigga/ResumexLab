from pathlib import Path
from typing import Optional
import os
import uuid
from datetime import datetime, date
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


def ensure_upload_dir():
    """Create upload directory if it doesn't exist"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def validate_file(file: UploadFile) -> bool:
    """Validate file extension and size"""
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False
    if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
        return False
    return True


def parse_date_string(date_str: Optional[str]) -> Optional[date]:
    """Parse date string to Python date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


async def save_upload_file(file: UploadFile) -> dict:
    """Save uploaded file and return attachment metadata dict"""
    ensure_upload_dir()
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    file_content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    return {
        "attachment_name": file.filename,
        "attachment_path": str(file_path),
        "attachment_size": len(file_content),
        "attachment_type": file.content_type,
        "attachment_url": f"/uploads/{unique_filename}",
    }


def delete_upload_file(file_path_str: Optional[str]) -> None:
    """Delete a file from the filesystem, ignoring missing files"""
    if not file_path_str:
        return
    path = Path(file_path_str)
    if path.exists():
        try:
            path.unlink()
        except Exception as e:
            print(f"Warning: Could not delete file {path}: {e}")
