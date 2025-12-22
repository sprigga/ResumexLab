from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class WorkExperienceBase(BaseModel):
    """Base work experience schema"""
    company_zh: Optional[str] = None
    company_en: Optional[str] = None
    position_zh: Optional[str] = None
    position_en: Optional[str] = None
    location_zh: Optional[str] = None
    location_en: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description_zh: Optional[str] = None
    description_en: Optional[str] = None
    display_order: int = 0
    # New attachment fields - added on 2025-12-22
    # Reason: Support file attachment functionality
    attachment_name: Optional[str] = None
    attachment_path: Optional[str] = None
    attachment_size: Optional[int] = None
    attachment_type: Optional[str] = None
    attachment_url: Optional[str] = None


class WorkExperienceCreate(WorkExperienceBase):
    """Work experience creation schema"""
    pass


class WorkExperienceUpdate(WorkExperienceBase):
    """Work experience update schema"""
    pass


# Modified on 2025-11-30: Separated WorkExperienceInDB without projects field first
# Reason: Avoid circular import, will use update_forward_refs after all schemas are loaded
class WorkExperienceInDB(WorkExperienceBase):
    """Work experience database schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Modified on 2025-11-30: Import ProjectInDB to avoid forward reference issues
# Reason: Include projects in work experience response
# Import after WorkExperienceInDB is defined to avoid circular dependency
from app.schemas.project import ProjectInDB

class WorkExperienceWithProjects(WorkExperienceInDB):
    """Work experience with projects included - use this for API responses"""
    projects: List[ProjectInDB] = Field(default_factory=list)

    class Config:
        from_attributes = True
