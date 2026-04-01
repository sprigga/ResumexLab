from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import logging
import os
from pathlib import Path
from app.db.base import get_db
from app.models.work_experience import WorkExperience
from app.schemas.work_experience import (
    WorkExperienceInDB,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    WorkExperienceWithProjects
)
from app.api.upload_utils import (
    UPLOAD_DIR,
    ensure_upload_dir,
    validate_file,
    parse_date_string,
    save_upload_file,
    delete_upload_file,
)
from app.api.endpoints.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


def _cleanup_stale_attachments(experiences: list, db: Session) -> int:
    """Clear attachment metadata for records whose files no longer exist on disk.

    Returns the number of records cleaned up.
    Added on 2026-04-01 to replace the side-effect logic removed from GET handlers
    (HIGH-1 fix: GET handlers must not write to the database).
    """
    cleaned = 0
    for exp in experiences:
        if exp.attachment_path and exp.attachment_url:
            if not os.path.isabs(exp.attachment_path):
                abs_path = UPLOAD_DIR / os.path.basename(exp.attachment_path)
            else:
                abs_path = Path(exp.attachment_path)

            if not abs_path.exists():
                logger.warning(
                    "Stale attachment reference found for work_experience id=%s path=%s — clearing",
                    exp.id,
                    exp.attachment_path,
                )
                exp.attachment_url = None
                exp.attachment_name = None
                exp.attachment_path = None
                exp.attachment_size = None
                exp.attachment_type = None
                cleaned += 1

    if cleaned:
        db.commit()

    return cleaned


# Modified on 2025-11-30: Changed response_model to WorkExperienceWithProjects
# Reason: Include projects in the API response
@router.get("/", response_model=List[WorkExperienceWithProjects])
async def get_work_experiences(db: Session = Depends(get_db)):
    """Get all work experiences with projects (public endpoint)"""
    experiences = db.query(WorkExperience)\
        .options(joinedload(WorkExperience.projects))\
        .order_by(WorkExperience.display_order)\
        .all()
    # Removed on 2026-04-01: attachment cleanup side effect (db.commit in GET)
    # Reason: HIGH-1 fix — GET handlers must be read-only; use POST /cleanup instead
    return experiences


@router.post("/cleanup", status_code=status.HTTP_200_OK)
async def cleanup_stale_attachments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admin endpoint: clear attachment metadata for records whose files no longer exist.

    Added on 2026-04-01 as part of HIGH-1 fix to replace the db.commit() side effects
    that were previously embedded in GET handlers.
    """
    experiences = db.query(WorkExperience).all()
    cleaned = _cleanup_stale_attachments(experiences, db)
    return {"cleaned": cleaned}


@router.post("/", response_model=WorkExperienceInDB, status_code=status.HTTP_201_CREATED)
async def create_work_experience(
    experience_data: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create work experience (requires authentication)"""
    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    try:
        db_experience = WorkExperience(**experience_data.model_dump())
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

# New file upload endpoint - added on 2025-12-22
# Reason: Handle file upload for work experience attachments
# Moved before GET /{experience_id} on 2026-04-01
# Reason: HIGH-2 fix — static routes must be registered before parameterized routes
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
    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    try:
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
            experience_data.update(await save_upload_file(file))

        # Create work experience
        db_experience = WorkExperience(**experience_data)
        db.add(db_experience)
        db.commit()
        db.refresh(db_experience)
        return db_experience
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")


# Modified on 2025-11-30: Changed response_model to WorkExperienceWithProjects
# Reason: Include projects in the API response
# Moved after static POST routes on 2026-04-01
# Reason: HIGH-2 fix — parameterized routes registered after static routes
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
    # Removed on 2026-04-01: attachment cleanup side effect (db.commit in GET)
    # Reason: HIGH-1 fix — GET handlers must be read-only; use POST /cleanup instead
    return experience


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
    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    try:
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
            "display_order": display_order,
            "description_zh": description_zh,
            "description_en": description_en,
            "start_date": parse_date_string(start_date),
            "end_date": parse_date_string(end_date),
            "is_current": is_current,
            "location_zh": location_zh,
            "location_en": location_en,
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

            delete_upload_file(experience.attachment_path)
            for key, value in (await save_upload_file(file)).items():
                setattr(experience, key, value)

        db.commit()
        db.refresh(experience)
        return experience
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

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

    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    try:
        update_data = experience_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(experience, field, value)

        db.commit()
        db.refresh(experience)
        return experience
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")


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

    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    try:
        # Delete associated file if exists - added on 2025-12-22
        # Reason: Clean up file system when deleting work experience
        delete_upload_file(experience.attachment_path)

        db.delete(experience)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
