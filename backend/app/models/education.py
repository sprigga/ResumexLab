from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Education(Base):
    """Education model"""
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_zh = Column(String(200))
    school_en = Column(String(200))
    degree_zh = Column(String(100))
    degree_en = Column(String(100))
    major_zh = Column(String(100))
    major_en = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description_zh = Column(Text)
    description_en = Column(Text)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
