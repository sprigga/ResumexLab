"""
Publications API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.publication import Publication
from app.schemas.publication import PublicationCreate, PublicationUpdate, PublicationResponse

router = APIRouter()


@router.get("/", response_model=List[PublicationResponse])
def get_publications(db: Session = Depends(get_db)):
    """Get all publications"""
    publications = db.query(Publication).order_by(Publication.display_order).all()
    return publications


@router.get("/{publication_id}", response_model=PublicationResponse)
def get_publication(publication_id: int, db: Session = Depends(get_db)):
    """Get a specific publication"""
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication


@router.post("/", response_model=PublicationResponse)
def create_publication(publication: PublicationCreate, db: Session = Depends(get_db)):
    """Create a new publication"""
    db_publication = Publication(**publication.dict())
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication


@router.put("/{publication_id}", response_model=PublicationResponse)
def update_publication(publication_id: int, publication: PublicationUpdate, db: Session = Depends(get_db)):
    """Update a publication"""
    db_publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not db_publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    for key, value in publication.dict(exclude_unset=True).items():
        setattr(db_publication, key, value)

    db.commit()
    db.refresh(db_publication)
    return db_publication


@router.delete("/{publication_id}")
def delete_publication(publication_id: int, db: Session = Depends(get_db)):
    """Delete a publication"""
    db_publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not db_publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    db.delete(db_publication)
    db.commit()
    return {"message": "Publication deleted successfully"}
