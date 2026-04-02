#!/bin/bash
# Entrypoint script for Resume Management System Backend
# Created: 2025-01-31
# Purpose: Handle database migrations and start the application

set -e

echo "=== Starting Backend Entrypoint ==="

# Wait a moment for filesystem to be ready
sleep 1

# --- Alembic revision guard ---
# 修改日期: 2026-04-02
# 說明: 檢查 DB 的 alembic_version 是否有對應的 migration 檔案。
#        若 revision 已被 squash 刪除，自動更新 alembic_version 為 head revision，
#        避免容器因 "Can't locate revision" 錯誤進入重啟迴圈。
python3 /app/alembic_guard.py /app/data/resume.db /app/alembic/versions
# --- End revision guard ---

echo "=== Running Alembic Migrations ==="

# Run alembic upgrade to head
# The migration file uses CREATE TABLE IF NOT EXISTS for idempotent migrations
# This allows safe re-running even if tables already exist
alembic upgrade head

echo "=== Migration Complete ==="
echo "=== Starting Application ==="

# Execute the main command (uvicorn)
exec "$@"
