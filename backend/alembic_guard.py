"""Alembic revision guard script.

检查 DB 的 alembic_version 是否有对应的 migration 文件。
若 revision 已被 squash 删除，自动将 alembic_version 更新为当前 head revision，
避免容器因 "Can't locate revision" 错误进入重启循环。

用法: python3 alembic_guard.py <db_path> <versions_dir>
"""
import sqlite3
import glob
import os
import re
import sys


def find_head_revision(versions_dir: str) -> str | None:
    """从 migration 文件中找出 head revision（没有 down_revision 指向它的 revision）。"""
    files = glob.glob(os.path.join(versions_dir, "*.py"))
    if not files:
        return None

    revisions: dict[str, str] = {}  # rev_id -> filename
    down_revisions: set[str] = set()

    for f in files:
        with open(f) as fh:
            content = fh.read()
        rev_match = re.search(r"revision:\s*str\s*=\s*'(\w+)'", content)
        if rev_match:
            rev_id = rev_match.group(1)
            revisions[rev_id] = f
        # 匹配 down_revision: Union[str, None] = '<id>' 或 down_revision = '<id>'
        for m in re.finditer(r"down_revision:\s*.*?=\s*['\"](\w+)['\"]", content):
            down_revisions.add(m.group(1))

    # head = 存在于 revisions 中但未被任何文件的 down_revision 引用
    heads = [r for r in revisions if r not in down_revisions]
    return heads[0] if heads else None


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 alembic_guard.py <db_path> <versions_dir>")
        sys.exit(1)

    db_path = sys.argv[1]
    versions_dir = sys.argv[2]

    if not os.path.isfile(db_path):
        return  # DB 不存在，无需检查

    # 读取当前 alembic_version
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.execute("SELECT version_num FROM alembic_version LIMIT 1")
        row = cur.fetchone()
        conn.close()
        current_rev = row[0] if row else ""
    except Exception:
        return  # 表不存在或 DB 损坏，交给 alembic upgrade 处理

    if not current_rev:
        return

    # 检查 migration 文件是否存在
    matching_files = glob.glob(os.path.join(versions_dir, f"{current_rev}*.py"))
    if matching_files:
        return  # 文件存在，无需修复

    # revision 文件不存在，需要修复
    print(f"⚠ WARNING: DB records revision '{current_rev}' but no matching migration file found.")
    print("  This usually happens after squashing migrations.")

    head = find_head_revision(versions_dir)
    if not head:
        print("  ERROR: Could not determine head revision. Manual fix required.")
        sys.exit(1)

    print(f"  Auto-fixing: updating alembic_version to '{head}'...")
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE alembic_version SET version_num = ?", (head,))
    conn.commit()
    conn.close()
    print(f"  ✓ alembic_version updated to '{head}'.")


if __name__ == "__main__":
    main()
