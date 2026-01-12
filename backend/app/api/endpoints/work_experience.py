from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import os
import uuid
from datetime import datetime, date
from pathlib import Path
from app.db.base import get_db
from app.models.work_experience import WorkExperience
from app.schemas.work_experience import (
    WorkExperienceInDB,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    WorkExperienceWithProjects  # Added on 2025-11-30
)
from app.api.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()

# File upload configuration - added on 2025-12-22
# Reason: Configure upload directory and allowed file types
import os
from pathlib import Path

# Use relative path for Docker container (uploads directory in container root)
# 已修改於 2025-01-12，原因：將檔案大小限制從 10MB 提高到 100MB
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def ensure_upload_dir():
    """Create upload directory if it doesn't exist"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def validate_file(file: UploadFile) -> bool:
    """Validate file type and size"""
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False

    # Check file size
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

# Modified on 2025-11-30: Changed response_model to WorkExperienceWithProjects
# Reason: Include projects in the API response
@router.get("/", response_model=List[WorkExperienceWithProjects])
async def get_work_experiences(db: Session = Depends(get_db)):
    """Get all work experiences with projects (public endpoint)"""
    experiences = db.query(WorkExperience)\
        .options(joinedload(WorkExperience.projects))\
        .order_by(WorkExperience.display_order)\
        .all()

    # Check attachment files exist and update URLs - added on 2025-12-22
    # Reason: Ensure attachment URLs are valid and files exist
    for exp in experiences:
        if exp.attachment_path and exp.attachment_url:
            # Convert relative path to absolute if needed
            if not os.path.isabs(exp.attachment_path):
                abs_path = UPLOAD_DIR / os.path.basename(exp.attachment_path)
            else:
                abs_path = Path(exp.attachment_path)
            
            # Check if file exists
            if not abs_path.exists():
                # File doesn't exist, clear attachment info
                exp.attachment_url = None
                exp.attachment_name = None
                exp.attachment_path = None
                exp.attachment_size = None
                exp.attachment_type = None
                # Update database
                db.commit()
            else:
                # Ensure URL is correct format
                filename = abs_path.name
                exp.attachment_url = f'/uploads/{filename}'
                # Update path to absolute path
                exp.attachment_path = str(abs_path)

    return experiences


# Modified on 2025-11-30: Changed response_model to WorkExperienceWithProjects
# Reason: Include projects in the API response
@router.get("/{experience_id}", response_model=WorkExperienceWithProjects)
async def get_work_experience(experience_id: int, db: Session = Depends(get_db)):
    """Get specific work experience with projects (public endpoint)"""
    experience = db.query(WorkExperience)\
        .options(joinedload(WorkExperience.projects))\
        .filter(WorkExperience.id == experience_id)\
        .first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found"
        )

    # Check attachment files exist and update URLs - added on 2025-12-22
    # Reason: Ensure attachment URLs are valid and files exist
    if experience.attachment_path and experience.attachment_url:
        # Convert relative path to absolute if needed
        if not os.path.isabs(experience.attachment_path):
            abs_path = UPLOAD_DIR / os.path.basename(experience.attachment_path)
        else:
            abs_path = Path(experience.attachment_path)
        
        # Check if file exists
        if not abs_path.exists():
            # File doesn't exist, clear attachment info
            experience.attachment_url = None
            experience.attachment_name = None
            experience.attachment_path = None
            experience.attachment_size = None
            experience.attachment_type = None
            # Update database
            db.commit()
        else:
            # Ensure URL is correct format
            filename = abs_path.name
            experience.attachment_url = f'/uploads/{filename}'
            # Update path to absolute path
            experience.attachment_path = str(abs_path)

    return experience


@router.post("/", response_model=WorkExperienceInDB, status_code=status.HTTP_201_CREATED)
async def create_work_experience(
    experience_data: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create work experience (requires authentication)"""
    db_experience = WorkExperience(**experience_data.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

# New file upload endpoint - added on 2025-12-22
# Reason: Handle file upload for work experience attachments
@router.post("/upload", response_model=WorkExperienceInDB, status_code=status.HTTP_201_CREATED)
async def create_work_experience_with_file(
    company_zh: Optional[str] = Form(None),
    company_en: Optional[str] = Form(None),
    position_zh: Optional[str] = Form(None),
    position_en: Optional[str] = Form(None),
    location_zh: Optional[str] = Form(None),
    location_en: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    is_current: bool = Form(False),
    description_zh: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    display_order: int = Form(0),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create work experience with file attachment"""
    # Validate file if provided
    if file and file.filename:
        if not validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type or size. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG. Max size: 100MB"
            )

    # Prepare experience data with proper date parsing - fixed on 2025-12-22
    # Reason: Convert date strings to Python date objects for SQLite compatibility
    experience_data = {
        "company_zh": company_zh,
        "company_en": company_en,
        "position_zh": position_zh,
        "position_en": position_en,
        "location_zh": location_zh,
        "location_en": location_en,
        "start_date": parse_date_string(start_date),
        "end_date": parse_date_string(end_date),
        "is_current": is_current,
        "description_zh": description_zh,
        "description_en": description_en,
        "display_order": display_order,
    }

    # Handle file upload
    if file and file.filename:
        ensure_upload_dir()

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        file_content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Add file info to experience data
        experience_data.update({
            "attachment_name": file.filename,
            "attachment_path": str(file_path),
            "attachment_size": len(file_content),
            "attachment_type": file.content_type,
            "attachment_url": f"/uploads/{unique_filename}"
        })

    # Create work experience
    db_experience = WorkExperience(**experience_data)
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


# New file upload update endpoint - added on 2025-12-22
# Reason: Handle file upload for work experience updates
@router.put("/{experience_id}/upload", response_model=WorkExperienceInDB)
async def update_work_experience_with_file(
    experience_id: int,
    company_zh: Optional[str] = Form(None),
    company_en: Optional[str] = Form(None),
    position_zh: Optional[str] = Form(None),
    position_en: Optional[str] = Form(None),
    location_zh: Optional[str] = Form(None),
    location_en: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    is_current: bool = Form(False),
    description_zh: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    display_order: int = Form(0),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update work experience with file attachment"""
    # Get existing experience
    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found"
        )

    # Prepare experience data with proper date parsing - fixed on 2025-12-22
    # Reason: Convert date strings to Python date objects for SQLite compatibility
    experience_data = {
        "company_zh": company_zh,
        "company_en": company_en,
        "position_zh": position_zh,
        "position_en": position_en,
        "location_zh": location_zh,
        "location_en": location_en,
        "start_date": parse_date_string(start_date),
        "end_date": parse_date_string(end_date),
        "is_current": is_current,
        "description_zh": description_zh,
        "description_en": description_en,
        "display_order": display_order,
    }

    # Update fields only if they are provided
    for field, value in experience_data.items():
        if value is not None:
            setattr(experience, field, value)

    # Handle file upload if provided
    if file and file.filename:
        # Validate file
        if not validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type or size. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG. Max size: 100MB"
            )

        # Delete old file if exists
        if experience.attachment_path:
            old_path = Path(experience.attachment_path)
            if old_path.exists():
                try:
                    old_path.unlink()
                except Exception as e:
                    print(f"Warning: Could not delete old file {old_path}: {e}")

        ensure_upload_dir()

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        file_content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Update file info
        experience.attachment_name = file.filename
        experience.attachment_path = str(file_path)
        experience.attachment_size = len(file_content)
        experience.attachment_type = file.content_type
        experience.attachment_url = f"/uploads/{unique_filename}"

    db.commit()
    db.refresh(experience)
    return experience

@router.put("/{experience_id}", response_model=WorkExperienceInDB)
async def update_work_experience(
    experience_id: int,
    experience_data: WorkExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update work experience (requires authentication)"""
    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found"
        )

    update_data = experience_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experience, field, value)

    db.commit()
    db.refresh(experience)
    return experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete work experience (requires authentication)"""
    experience = db.query(WorkExperience).filter(WorkExperience.id == experience_id).first()

    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found"
        )

    # Delete associated file if exists - added on 2025-12-22
    # Reason: Clean up file system when deleting work experience
    if experience.attachment_path:
        file_path = Path(experience.attachment_path)
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                # Log error but continue with deletion
                print(f"Warning: Could not delete file {file_path}: {e}")

    db.delete(experience)
    db.commit()
    return None
