from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    """Project model"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    work_experience_id = Column(Integer, ForeignKey("work_experience.id"), nullable=True)
    title_zh = Column(String(200))
    title_en = Column(String(200))
    description_zh = Column(Text)
    description_en = Column(Text)
    technologies = Column(Text)  # JSON format
    tools = Column(Text)  # JSON format
    environment = Column(Text)  # JSON format
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    display_order = Column(Integer, default=0)
    # New attachment fields - added on 2025-12-22
    # Reason: Support file attachment functionality similar to work experience
    attachment_name = Column(String(255))
    attachment_path = Column(String(500))
    attachment_size = Column(Integer)
    attachment_type = Column(String(100))
    attachment_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    work_experience = relationship("WorkExperience", back_populates="projects")
    details = relationship("ProjectDetail", back_populates="project", cascade="all, delete-orphan", order_by="ProjectDetail.display_order")


class ProjectDetail(Base):
    """Project detail model - 專案細節描述（支援 HTML 格式）"""
    __tablename__ = "project_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    # Modified on 2025-11-30: 改為支援 HTML 格式的描述欄位
    description_zh = Column(Text)  # HTML format supported
    description_en = Column(Text)  # HTML format supported
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="details")
    attachments = relationship("ProjectAttachment", back_populates="project_detail", cascade="all, delete-orphan", order_by="ProjectAttachment.display_order")


class ProjectAttachment(Base):
    """Project attachment model - 專案附件（檔案連結）"""
    __tablename__ = "project_attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_detail_id = Column(Integer, ForeignKey("project_details.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)  # 檔案連結
    file_type = Column(String(50), nullable=False)  # jpg, png, bmp, pdf, word, excel, powerpoint, text, html
    file_size = Column(Integer, nullable=True)  # 檔案大小（bytes）
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    project_detail = relationship("ProjectDetail", back_populates="attachments")
