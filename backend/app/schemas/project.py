from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# ===== ProjectAttachment Schemas =====

class ProjectAttachmentBase(BaseModel):
    """Base project attachment schema"""
    file_name: str
    file_url: str
    file_type: str  # jpg, png, bmp, pdf, word, excel, powerpoint, text, html
    file_size: Optional[int] = None
    display_order: int = 0


class ProjectAttachmentCreate(ProjectAttachmentBase):
    """Project attachment creation schema"""
    pass


class ProjectAttachmentUpdate(ProjectAttachmentBase):
    """Project attachment update schema"""
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None


class ProjectAttachmentInDB(ProjectAttachmentBase):
    """Project attachment database schema"""
    id: int
    project_detail_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== ProjectDetail Schemas =====

class ProjectDetailBase(BaseModel):
    """Base project detail schema - 支援 HTML 格式的專案描述"""
    description_zh: Optional[str] = None  # HTML format supported
    description_en: Optional[str] = None  # HTML format supported
    display_order: int = 0


class ProjectDetailCreate(ProjectDetailBase):
    """Project detail creation schema"""
    attachments: Optional[List[ProjectAttachmentCreate]] = []


class ProjectDetailUpdate(ProjectDetailBase):
    """Project detail update schema"""
    attachments: Optional[List[ProjectAttachmentCreate]] = None


class ProjectDetailInDB(ProjectDetailBase):
    """Project detail database schema"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    attachments: List[ProjectAttachmentInDB] = []

    class Config:
        from_attributes = True


# ===== Project Schemas =====

class ProjectBase(BaseModel):
    """Base project schema"""
    title_zh: Optional[str] = None
    title_en: Optional[str] = None
    description_zh: Optional[str] = None
    description_en: Optional[str] = None
    technologies: Optional[str] = None  # JSON format
    tools: Optional[str] = None  # JSON format
    environment: Optional[str] = None  # JSON format
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    display_order: int = 0


class ProjectCreate(ProjectBase):
    """Project creation schema"""
    work_experience_id: Optional[int] = None
    details: Optional[List[ProjectDetailCreate]] = []


class ProjectUpdate(ProjectBase):
    """Project update schema"""
    work_experience_id: Optional[int] = None
    details: Optional[List[ProjectDetailCreate]] = None


class ProjectInDB(ProjectBase):
    """Project database schema"""
    id: int
    work_experience_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    details: List[ProjectDetailInDB] = []

    class Config:
        from_attributes = True


# 已新增於 2025-11-30，原因：為 API 端點添加回應 schema
class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: int
    work_experience_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
