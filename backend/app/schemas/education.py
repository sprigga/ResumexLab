"""
Education schemas
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class EducationBase(BaseModel):
    """Base education schema"""
    school_zh: Optional[str] = None
    school_en: Optional[str] = None
    degree_zh: Optional[str] = None
    degree_en: Optional[str] = None
    major_zh: Optional[str] = None
    major_en: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description_zh: Optional[str] = None
    description_en: Optional[str] = None
    display_order: int = 0


class EducationCreate(EducationBase):
    """Education creation schema"""
    pass


class EducationUpdate(EducationBase):
    """Education update schema"""
    pass


class EducationResponse(EducationBase):
    """Education response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
