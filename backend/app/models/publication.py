from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Publication(Base):
    """Academic publication model"""
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text)
    authors = Column(Text)
    publication = Column(Text)
    year = Column(Integer)
    pages = Column(String(50))
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GithubProject(Base):
    """GitHub project model"""
    __tablename__ = "github_projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_zh = Column(String(200))
    name_en = Column(String(200))
    description_zh = Column(Text)
    description_en = Column(Text)
    url = Column(Text)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
