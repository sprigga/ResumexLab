"""
Certifications API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.certification import Certification
from app.schemas.certification import CertificationCreate, CertificationUpdate, CertificationResponse

router = APIRouter()


@router.get("/", response_model=List[CertificationResponse])
def get_certifications(db: Session = Depends(get_db)):
    """Get all certifications"""
    certifications = db.query(Certification).order_by(Certification.display_order).all()
    return certifications


@router.get("/{certification_id}", response_model=CertificationResponse)
def get_certification(certification_id: int, db: Session = Depends(get_db)):
    """Get a specific certification"""
    certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not certification:
        raise HTTPException(status_code=404, detail="Certification not found")
    return certification


@router.post("/", response_model=CertificationResponse)
def create_certification(certification: CertificationCreate, db: Session = Depends(get_db)):
    """Create a new certification"""
    db_certification = Certification(**certification.dict())
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    return db_certification


@router.put("/{certification_id}", response_model=CertificationResponse)
def update_certification(certification_id: int, certification: CertificationUpdate, db: Session = Depends(get_db)):
    """Update a certification"""
    db_certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not db_certification:
        raise HTTPException(status_code=404, detail="Certification not found")

    for key, value in certification.dict(exclude_unset=True).items():
        setattr(db_certification, key, value)

    db.commit()
    db.refresh(db_certification)
    return db_certification


@router.delete("/{certification_id}")
def delete_certification(certification_id: int, db: Session = Depends(get_db)):
    """Delete a certification"""
    db_certification = db.query(Certification).filter(Certification.id == certification_id).first()
    if not db_certification:
        raise HTTPException(status_code=404, detail="Certification not found")

    db.delete(db_certification)
    db.commit()
    return {"message": "Certification deleted successfully"}
