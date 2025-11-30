"""
Education API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationUpdate, EducationResponse

router = APIRouter()


@router.get("/", response_model=List[EducationResponse])
def get_education(db: Session = Depends(get_db)):
    """Get all education records"""
    education = db.query(Education).order_by(Education.display_order).all()
    return education


@router.get("/{education_id}", response_model=EducationResponse)
def get_education_item(education_id: int, db: Session = Depends(get_db)):
    """Get a specific education record"""
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    return education


@router.post("/", response_model=EducationResponse)
def create_education(education: EducationCreate, db: Session = Depends(get_db)):
    """Create a new education record"""
    db_education = Education(**education.dict())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@router.put("/{education_id}", response_model=EducationResponse)
def update_education(education_id: int, education: EducationUpdate, db: Session = Depends(get_db)):
    """Update an education record"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="Education record not found")

    for key, value in education.dict(exclude_unset=True).items():
        setattr(db_education, key, value)

    db.commit()
    db.refresh(db_education)
    return db_education


@router.delete("/{education_id}")
def delete_education(education_id: int, db: Session = Depends(get_db)):
    """Delete an education record"""
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if not db_education:
        raise HTTPException(status_code=404, detail="Education record not found")

    db.delete(db_education)
    db.commit()
    return {"message": "Education record deleted successfully"}
