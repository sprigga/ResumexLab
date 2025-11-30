"""
Publication and GitHub Project schemas
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ===== Publication Schemas =====

class PublicationBase(BaseModel):
    """Base publication schema"""
    title: Optional[str] = None
    authors: Optional[str] = None
    publication: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[str] = None
    display_order: int = 0


class PublicationCreate(PublicationBase):
    """Publication creation schema"""
    pass


class PublicationUpdate(PublicationBase):
    """Publication update schema"""
    pass


class PublicationResponse(PublicationBase):
    """Publication response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== GitHub Project Schemas =====

class GithubProjectBase(BaseModel):
    """Base GitHub project schema"""
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    description_zh: Optional[str] = None
    description_en: Optional[str] = None
    url: Optional[str] = None
    display_order: int = 0


class GithubProjectCreate(GithubProjectBase):
    """GitHub project creation schema"""
    pass


class GithubProjectUpdate(GithubProjectBase):
    """GitHub project update schema"""
    pass


class GithubProjectResponse(GithubProjectBase):
    """GitHub project response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
