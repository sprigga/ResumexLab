"""
Certification and Language schemas
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# ===== Certification Schemas =====

class CertificationBase(BaseModel):
    """Base certification schema"""
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[date] = None
    certificate_number: Optional[str] = None
    display_order: int = 0


class CertificationCreate(CertificationBase):
    """Certification creation schema"""
    pass


class CertificationUpdate(CertificationBase):
    """Certification update schema"""
    pass


class CertificationResponse(CertificationBase):
    """Certification response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== Language Schemas =====

class LanguageBase(BaseModel):
    """Base language schema"""
    language_zh: Optional[str] = None
    language_en: Optional[str] = None
    proficiency_zh: Optional[str] = None
    proficiency_en: Optional[str] = None
    test_name: Optional[str] = None
    score: Optional[str] = None
    display_order: int = 0


class LanguageCreate(LanguageBase):
    """Language creation schema"""
    pass


class LanguageUpdate(LanguageBase):
    """Language update schema"""
    pass


class LanguageResponse(LanguageBase):
    """Language response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
