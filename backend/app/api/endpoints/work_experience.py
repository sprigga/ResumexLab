from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
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


# Modified on 2025-11-30: Changed response_model to WorkExperienceWithProjects
# Reason: Include projects in the API response
@router.get("/", response_model=List[WorkExperienceWithProjects])
async def get_work_experiences(db: Session = Depends(get_db)):
    """Get all work experiences with projects (public endpoint)"""
    experiences = db.query(WorkExperience)\
        .options(joinedload(WorkExperience.projects))\
        .order_by(WorkExperience.display_order)\
        .all()
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

    db.delete(experience)
    db.commit()
    return None
