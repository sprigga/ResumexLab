from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Certification(Base):
    """Certification model"""
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_zh = Column(String(200))
    name_en = Column(String(200))
    issuer = Column(String(200))
    issue_date = Column(Date)
    certificate_number = Column(String(100))
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Language(Base):
    """Language proficiency model"""
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    language_zh = Column(String(50))
    language_en = Column(String(50))
    proficiency_zh = Column(String(50))
    proficiency_en = Column(String(50))
    test_name = Column(String(100))
    score = Column(String(50))
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
