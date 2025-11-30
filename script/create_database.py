"""
Script to create database tables
Author: Polo (林鴻全)
Date: 2025-11-29
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.db.base import Base, engine
from app.models.user import User
from app.models.personal_info import PersonalInfo
from app.models.work_experience import WorkExperience
from app.models.project import Project, ProjectDetail
from app.models.education import Education
from app.models.certification import Certification, Language
from app.models.publication import Publication, GithubProject


def create_tables():
    """建立所有資料表"""
    print("正在建立資料庫表格...")
    Base.metadata.create_all(bind=engine)
    print("✓ 資料庫表格建立完成")


if __name__ == "__main__":
    create_tables()
