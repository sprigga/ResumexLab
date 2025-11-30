from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PersonalInfoBase(BaseModel):
    """Base personal info schema"""
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address_zh: Optional[str] = None
    address_en: Optional[str] = None
    objective_zh: Optional[str] = None
    objective_en: Optional[str] = None
    personality_zh: Optional[str] = None
    personality_en: Optional[str] = None
    summary_zh: Optional[str] = None
    summary_en: Optional[str] = None


class PersonalInfoCreate(PersonalInfoBase):
    """Personal info creation schema"""
    pass


class PersonalInfoUpdate(PersonalInfoBase):
    """Personal info update schema"""
    pass


class PersonalInfoInDB(PersonalInfoBase):
    """Personal info database schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
