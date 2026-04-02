"""初始化資料庫表（含附件欄位）

Revision ID: d711f173f9e3
Revises:
Create Date: 2025-12-30 16:34:52.165934

Modified: 2026-02-18
Reason: Added IF NOT EXISTS clauses to make migration idempotent.
This fixes the "table already exists" error when both Alembic and
SQLAlchemy's Base.metadata.create_all() try to create tables.

Squash: 2026-04-01
此 migration 已合併原 ce10aaa23747（添加附件欄位到 work_experience 和 projects 表）的內容。
work_experience 和 projects 表的 attachment_* 欄位（attachment_name、attachment_path、
attachment_size、attachment_type、attachment_url）從一開始就包含在本 migration 中，
ce10aaa23747 是歷史遺留的冗餘 migration，已刪除。
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd711f173f9e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    # Use CREATE TABLE IF NOT EXISTS for idempotent migrations
    # This allows the migration to run safely even if tables already exist
    # (e.g., when Base.metadata.create_all() runs before Alembic)

    # certifications table
    op.execute("""
        CREATE TABLE IF NOT EXISTS certifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_zh VARCHAR(200),
            name_en VARCHAR(200),
            issuer VARCHAR(200),
            issue_date DATE,
            certificate_number VARCHAR(100),
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_certifications_id ON certifications (id)")

    # education table
    op.execute("""
        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_zh VARCHAR(200),
            school_en VARCHAR(200),
            degree_zh VARCHAR(100),
            degree_en VARCHAR(100),
            major_zh VARCHAR(100),
            major_en VARCHAR(100),
            start_date DATE,
            end_date DATE,
            description_zh TEXT,
            description_en TEXT,
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_education_id ON education (id)")

    # github_projects table
    op.execute("""
        CREATE TABLE IF NOT EXISTS github_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_zh VARCHAR(200),
            name_en VARCHAR(200),
            description_zh TEXT,
            description_en TEXT,
            url TEXT,
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_github_projects_id ON github_projects (id)")

    # languages table
    op.execute("""
        CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language_zh VARCHAR(50),
            language_en VARCHAR(50),
            proficiency_zh VARCHAR(50),
            proficiency_en VARCHAR(50),
            test_name VARCHAR(100),
            score VARCHAR(50),
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_languages_id ON languages (id)")

    # personal_info table
    op.execute("""
        CREATE TABLE IF NOT EXISTS personal_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_zh VARCHAR(100),
            name_en VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100),
            address_zh TEXT,
            address_en TEXT,
            objective_zh TEXT,
            objective_en TEXT,
            personality_zh TEXT,
            personality_en TEXT,
            summary_zh TEXT,
            summary_en TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_personal_info_id ON personal_info (id)")

    # publications table
    op.execute("""
        CREATE TABLE IF NOT EXISTS publications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            authors TEXT,
            publication TEXT,
            year INTEGER,
            pages VARCHAR(50),
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_publications_id ON publications (id)")

    # users table
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (username)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_username ON users (username)")

    # work_experience table
    op.execute("""
        CREATE TABLE IF NOT EXISTS work_experience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_zh VARCHAR(200),
            company_en VARCHAR(200),
            position_zh VARCHAR(100),
            position_en VARCHAR(100),
            location_zh VARCHAR(100),
            location_en VARCHAR(100),
            start_date DATE,
            end_date DATE,
            is_current BOOLEAN,
            description_zh TEXT,
            description_en TEXT,
            display_order INTEGER,
            attachment_name VARCHAR(255),
            attachment_path VARCHAR(500),
            attachment_size INTEGER,
            attachment_type VARCHAR(100),
            attachment_url VARCHAR(500),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_work_experience_id ON work_experience (id)")

    # projects table
    op.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_experience_id INTEGER,
            title_zh VARCHAR(200),
            title_en VARCHAR(200),
            description_zh TEXT,
            description_en TEXT,
            technologies TEXT,
            tools TEXT,
            environment TEXT,
            start_date DATE,
            end_date DATE,
            display_order INTEGER,
            attachment_name VARCHAR(255),
            attachment_path VARCHAR(500),
            attachment_size INTEGER,
            attachment_type VARCHAR(100),
            attachment_url VARCHAR(500),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (work_experience_id) REFERENCES work_experience (id)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_projects_id ON projects (id)")

    # project_details table
    op.execute("""
        CREATE TABLE IF NOT EXISTS project_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            description_zh TEXT,
            description_en TEXT,
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_project_details_id ON project_details (id)")

    # project_attachments table
    op.execute("""
        CREATE TABLE IF NOT EXISTS project_attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_detail_id INTEGER NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_url TEXT NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            file_size INTEGER,
            display_order INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_detail_id) REFERENCES project_details (id)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_project_attachments_id ON project_attachments (id)")


def downgrade() -> None:
    # Drop in reverse order of creation (to handle foreign key constraints)
    op.execute("DROP INDEX IF EXISTS ix_project_attachments_id")
    op.execute("DROP TABLE IF EXISTS project_attachments")

    op.execute("DROP INDEX IF EXISTS ix_project_details_id")
    op.execute("DROP TABLE IF EXISTS project_details")

    op.execute("DROP INDEX IF EXISTS ix_projects_id")
    op.execute("DROP TABLE IF EXISTS projects")

    op.execute("DROP INDEX IF EXISTS ix_users_username")
    op.execute("DROP INDEX IF EXISTS ix_users_id")
    op.execute("DROP TABLE IF EXISTS users")

    op.execute("DROP INDEX IF EXISTS ix_publications_id")
    op.execute("DROP TABLE IF EXISTS publications")

    op.execute("DROP INDEX IF EXISTS ix_personal_info_id")
    op.execute("DROP TABLE IF EXISTS personal_info")

    op.execute("DROP INDEX IF EXISTS ix_languages_id")
    op.execute("DROP TABLE IF EXISTS languages")

    op.execute("DROP INDEX IF EXISTS ix_github_projects_id")
    op.execute("DROP TABLE IF EXISTS github_projects")

    op.execute("DROP INDEX IF EXISTS ix_education_id")
    op.execute("DROP TABLE IF EXISTS education")

    op.execute("DROP INDEX IF EXISTS ix_certifications_id")
    op.execute("DROP TABLE IF EXISTS certifications")
