"""
資料庫遷移腳本: 更新 project_details 表並新增 project_attachments 表

Created on: 2025-11-30
Purpose:
1. 將 project_details.detail_zh 重命名為 description_zh
2. 將 project_details.detail_en 重命名為 description_en
3. 新增 project_details.updated_at 欄位
4. 創建新的 project_attachments 表

使用方法:
    cd /Users/pololin/python_project/resumexlab
    source backend/.venv/bin/activate
    python script/migrate_project_details.py
"""

import sys
import os

# 加入 backend 路徑以便導入模組
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_path)

from sqlalchemy import create_engine, text
from app.core.config import settings


def migrate_database():
    """執行資料庫遷移"""

    # 創建資料庫連接
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    print("開始資料庫遷移...")
    print(f"資料庫位置: {settings.DATABASE_URL}")

    with engine.connect() as connection:
        # 開始交易
        trans = connection.begin()

        try:
            # 1. 檢查 project_details 表是否存在舊欄位
            result = connection.execute(text(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='project_details'"
            ))
            table_schema = result.fetchone()

            if table_schema:
                schema_sql = table_schema[0]
                print(f"\n目前的 project_details 表結構:\n{schema_sql}\n")

                # 檢查是否需要遷移
                if 'detail_zh' in schema_sql or 'detail_en' in schema_sql:
                    print("偵測到舊欄位名稱 (detail_zh, detail_en)，開始遷移...")

                    # SQLite 不支援直接 ALTER COLUMN，需要重建表
                    # 步驟: 創建新表 -> 複製資料 -> 刪除舊表 -> 重命名新表

                    # 創建暫存表
                    connection.execute(text("""
                        CREATE TABLE project_details_new (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            project_id INTEGER NOT NULL,
                            description_zh TEXT,
                            description_en TEXT,
                            display_order INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (project_id) REFERENCES projects(id)
                        )
                    """))
                    print("✓ 已創建新的 project_details 表結構")

                    # 複製資料 (處理可能的欄位名稱差異)
                    if 'detail_zh' in schema_sql:
                        connection.execute(text("""
                            INSERT INTO project_details_new
                                (id, project_id, description_zh, description_en, display_order, created_at)
                            SELECT
                                id, project_id, detail_zh, detail_en, display_order, created_at
                            FROM project_details
                        """))
                    else:
                        connection.execute(text("""
                            INSERT INTO project_details_new
                                (id, project_id, description_zh, description_en, display_order, created_at)
                            SELECT
                                id, project_id, description_zh, description_en, display_order, created_at
                            FROM project_details
                        """))
                    print("✓ 已複製現有資料")

                    # 刪除舊表
                    connection.execute(text("DROP TABLE project_details"))
                    print("✓ 已刪除舊表")

                    # 重命名新表
                    connection.execute(text("ALTER TABLE project_details_new RENAME TO project_details"))
                    print("✓ 已重命名新表")
                else:
                    print("project_details 表已經是最新結構，跳過遷移")
            else:
                print("project_details 表不存在，將由系統自動創建")

            # 2. 創建 project_attachments 表（如果不存在）
            result = connection.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='project_attachments'"
            ))

            if not result.fetchone():
                connection.execute(text("""
                    CREATE TABLE project_attachments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_detail_id INTEGER NOT NULL,
                        file_name VARCHAR(255) NOT NULL,
                        file_url TEXT NOT NULL,
                        file_type VARCHAR(50) NOT NULL,
                        file_size INTEGER,
                        display_order INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (project_detail_id) REFERENCES project_details(id)
                    )
                """))
                print("✓ 已創建 project_attachments 表")
            else:
                print("project_attachments 表已存在，跳過創建")

            # 提交交易
            trans.commit()
            print("\n✓ 資料庫遷移完成!")

        except Exception as e:
            # 發生錯誤時回滾
            trans.rollback()
            print(f"\n✗ 遷移失敗: {str(e)}")
            raise

    # 顯示最終的表結構
    with engine.connect() as connection:
        print("\n=== 遷移後的表結構 ===")

        result = connection.execute(text(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='project_details'"
        ))
        table = result.fetchone()
        if table:
            print(f"\nproject_details:\n{table[0]}\n")

        result = connection.execute(text(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='project_attachments'"
        ))
        table = result.fetchone()
        if table:
            print(f"\nproject_attachments:\n{table[0]}\n")


if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"\n遷移過程發生錯誤: {str(e)}")
        sys.exit(1)
