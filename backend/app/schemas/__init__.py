# Modified on 2025-11-30: °ž project schemas
from app.schemas.user import UserBase, UserCreate, UserInDB
from app.schemas.personal_info import PersonalInfoBase, PersonalInfoCreate, PersonalInfoUpdate, PersonalInfoInDB
from app.schemas.work_experience import WorkExperienceBase, WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceInDB
from app.schemas.project import (
    ProjectBase, ProjectCreate, ProjectUpdate, ProjectInDB,
    ProjectDetailBase, ProjectDetailCreate, ProjectDetailUpdate, ProjectDetailInDB,
    ProjectAttachmentBase, ProjectAttachmentCreate, ProjectAttachmentUpdate, ProjectAttachmentInDB
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserInDB",
    # Personal info schemas
    "PersonalInfoBase",
    "PersonalInfoCreate",
    "PersonalInfoUpdate",
    "PersonalInfoInDB",
    # Work experience schemas
    "WorkExperienceBase",
    "WorkExperienceCreate",
    "WorkExperienceUpdate",
    "WorkExperienceInDB",
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectInDB",
    "ProjectDetailBase",
    "ProjectDetailCreate",
    "ProjectDetailUpdate",
    "ProjectDetailInDB",
    "ProjectAttachmentBase",
    "ProjectAttachmentCreate",
    "ProjectAttachmentUpdate",
    "ProjectAttachmentInDB",
]
