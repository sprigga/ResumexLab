"""
Languages API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.certification import Language
from app.schemas.certification import LanguageCreate, LanguageUpdate, LanguageResponse

router = APIRouter()


@router.get("/", response_model=List[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    """Get all languages"""
    languages = db.query(Language).order_by(Language.display_order).all()
    return languages


@router.get("/{language_id}", response_model=LanguageResponse)
def get_language(language_id: int, db: Session = Depends(get_db)):
    """Get a specific language"""
    language = db.query(Language).filter(Language.id == language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.post("/", response_model=LanguageResponse)
def create_language(language: LanguageCreate, db: Session = Depends(get_db)):
    """Create a new language"""
    db_language = Language(**language.dict())
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


@router.put("/{language_id}", response_model=LanguageResponse)
def update_language(language_id: int, language: LanguageUpdate, db: Session = Depends(get_db)):
    """Update a language"""
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if not db_language:
        raise HTTPException(status_code=404, detail="Language not found")

    for key, value in language.dict(exclude_unset=True).items():
        setattr(db_language, key, value)

    db.commit()
    db.refresh(db_language)
    return db_language


@router.delete("/{language_id}")
def delete_language(language_id: int, db: Session = Depends(get_db)):
    """Delete a language"""
    db_language = db.query(Language).filter(Language.id == language_id).first()
    if not db_language:
        raise HTTPException(status_code=404, detail="Language not found")

    db.delete(db_language)
    db.commit()
    return {"message": "Language deleted successfully"}
