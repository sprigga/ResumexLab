"""
Script to create database tables
Author: Polo (林鴻全)
Date: 2025-11-29
Updated: 2025-12-01 - 新增資料庫目錄檢查和建立功能
"""

import sys
from pathlib import Path
import os
import re

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


def ensure_database_directory():
    """確保資料庫目錄存在，若不存在則建立"""
    # 從 settings 取得資料庫 URL
    from app.core.config import settings
    database_url = settings.DATABASE_URL

    # 解析 SQLite 資料庫路徑 (格式: sqlite:///./data/resume.db)
    # 使用正則表達式提取路徑部分
    match = re.match(r'sqlite:///\./(.*)', database_url)
    if match:
        db_path = match.group(1)  # 例如: data/resume.db
        db_dir = os.path.dirname(db_path)  # 例如: data

        if db_dir and not os.path.exists(db_dir):
            print(f"資料庫目錄 '{db_dir}' 不存在，正在建立...")
            os.makedirs(db_dir, exist_ok=True)
            print(f"✓ 資料庫目錄 '{db_dir}' 建立成功")
        else:
            print(f"✓ 資料庫目錄 '{db_dir}' 已存在")
    else:
        print("⚠ 無法解析資料庫路徑，跳過目錄檢查")


def create_tables():
    """建立所有資料表"""
    # 先確保資料庫目錄存在
    ensure_database_directory()

    print("正在建立資料庫表格...")
    Base.metadata.create_all(bind=engine)
    print("✓ 資料庫表格建立完成")


if __name__ == "__main__":
    create_tables()
