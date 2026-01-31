"""
Projects API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form, Body
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime, date
from pathlib import Path

from app.db.base import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter()

# File upload configuration - added on 2025-12-22
# Reason: Configure upload directory and allowed file types for projects
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

@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(Project).order_by(Project.display_order).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}


# New file upload creation endpoint - added on 2025-12-22
# Reason: Handle file upload for project creation
@router.post("/upload", response_model=ProjectResponse)
async def create_project_with_file(
    work_experience_id: Optional[int] = Form(None),
    title_zh: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    description_zh: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    technologies: Optional[str] = Form(None),
    tools: Optional[str] = Form(None),
    environment: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    display_order: int = Form(0),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create project with file attachment"""
    # Validate file if provided
    if file and file.filename:
        if not validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type or size. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG. Max size: 100MB"
            )

    # Prepare project data with proper date parsing - fixed on 2025-12-22
    # Reason: Convert date strings to Python date objects for SQLite compatibility
    project_data = {
        "work_experience_id": work_experience_id,
        "title_zh": title_zh,
        "title_en": title_en,
        "description_zh": description_zh,
        "description_en": description_en,
        "technologies": technologies,
        "tools": tools,
        "environment": environment,
        "start_date": parse_date_string(start_date),
        "end_date": parse_date_string(end_date),
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

        # Add file info to project data
        project_data.update({
            "attachment_name": file.filename,
            "attachment_path": str(file_path),
            "attachment_size": len(file_content),
            "attachment_type": file.content_type,
            "attachment_url": f"/uploads/{unique_filename}"
        })

    # Create project
    db_project = Project(**project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# New file upload update endpoint - added on 2025-12-22
# Reason: Handle file upload for project updates
@router.put("/{project_id}/upload", response_model=ProjectResponse)
async def update_project_with_file(
    project_id: int,
    work_experience_id: Optional[int] = Form(None),
    title_zh: Optional[str] = Form(None),
    title_en: Optional[str] = Form(None),
    description_zh: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    technologies: Optional[str] = Form(None),
    tools: Optional[str] = Form(None),
    environment: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    display_order: int = Form(0),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Update project with file attachment"""
    # Get existing project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Validate file if provided
    if file and file.filename:
        if not validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type or size. Allowed types: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG. Max size: 100MB"
            )

    # Prepare project data with proper date parsing - fixed on 2025-12-22
    # Reason: Convert date strings to Python date objects for SQLite compatibility
    project_data = {
        "work_experience_id": work_experience_id,
        "title_zh": title_zh,
        "title_en": title_en,
        "description_zh": description_zh,
        "description_en": description_en,
        "technologies": technologies,
        "tools": tools,
        "environment": environment,
        "start_date": parse_date_string(start_date),
        "end_date": parse_date_string(end_date),
        "display_order": display_order,
    }

    # Handle file upload
    if file and file.filename:
        ensure_upload_dir()

        # Delete old file if exists
        if project.attachment_path and os.path.exists(project.attachment_path):
            try:
                os.remove(project.attachment_path)
            except OSError:
                pass

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        file_content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Add file info to project data
        project_data.update({
            "attachment_name": file.filename,
            "attachment_path": str(file_path),
            "attachment_size": len(file_content),
            "attachment_type": file.content_type,
            "attachment_url": f"/uploads/{unique_filename}"
        })
    else:
        # Clear attachment info if no file provided
        project_data.update({
            "attachment_name": None,
            "attachment_path": None,
            "attachment_size": None,
            "attachment_type": None,
            "attachment_url": None
        })

    # Update project
    for key, value in project_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


# New endpoint to update attachment name only - added on 2025-01-15
# Reason: Allow updating attachment display name without uploading a new file
# Modified on 2025-01-15: Changed from Form to Body for better compatibility with axios
@router.patch("/{project_id}/attachment-name", response_model=ProjectResponse)
def update_project_attachment_name(
    project_id: int,
    attachment_name: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Update only the attachment_name field of a project

    This allows changing the display name of an attachment without
    uploading a new file or modifying other project fields.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Received attachment_name update request: project_id={project_id}, attachment_name={attachment_name}")

    # Get existing project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Update only the attachment_name field
    project.attachment_name = attachment_name

    db.commit()
    db.refresh(project)
    logger.info(f"Updated attachment_name for project {project_id} to '{attachment_name}'")
    return project
