from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class PersonalInfo(Base):
    """Personal information model"""
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_zh = Column(String(100))
    name_en = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address_zh = Column(Text)
    address_en = Column(Text)
    objective_zh = Column(Text)
    objective_en = Column(Text)
    personality_zh = Column(Text)
    personality_en = Column(Text)
    summary_zh = Column(Text)
    summary_en = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
