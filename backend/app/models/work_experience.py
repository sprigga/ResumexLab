from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class WorkExperience(Base):
    """Work experience model"""
    __tablename__ = "work_experience"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_zh = Column(String(200))
    company_en = Column(String(200))
    position_zh = Column(String(100))
    position_en = Column(String(100))
    location_zh = Column(String(100))
    location_en = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    description_zh = Column(Text)
    description_en = Column(Text)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to projects
    projects = relationship("Project", back_populates="work_experience", cascade="all, delete-orphan")
