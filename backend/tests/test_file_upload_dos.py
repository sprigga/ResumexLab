"""
Tests for P0 Fix #2: File Upload DoS Vulnerability
CVSS 7.5 - Confirms the database import endpoint rejects oversized files
before reading them into memory.

MAX_DB_FILE_SIZE = 100MB (set in import_data.py)
"""
import io
import os
import sqlite3
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch


DB_IMPORT_URL = "/api/import/database/import/"


def _make_minimal_sqlite_db() -> bytes:
    """Create a valid (but empty) SQLite database file and return its bytes."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        conn = sqlite3.connect(tmp_path)
        conn.close()
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_non_db_file_rejected(client):
    """
    A file that doesn't end in .db must be rejected with 400.
    This is checked BEFORE reading file content (fastest rejection).
    No file is written to disk.
    """
    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("resume.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
    )
    assert response.status_code == 400, (
        f"Expected 400 for non-.db file, got {response.status_code}: {response.text}"
    )


def test_oversized_file_rejected(client):
    """
    A .db file larger than 100MB must be rejected with 413.
    Uses 101MB to definitely exceed the limit.
    The file.size header check catches this BEFORE reading the body.
    No file is written to disk (rejected before I/O).
    """
    OVER_LIMIT = 101 * 1024 * 1024  # 101MB
    fake_content = b"x" * OVER_LIMIT

    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("big_file.db", io.BytesIO(fake_content), "application/octet-stream")}
    )
    assert response.status_code == 413, (
        f"Expected 413 for oversized file, got {response.status_code}: {response.text}"
    )


def test_small_db_file_passes_size_check(client, tmp_path, monkeypatch):
    """
    A small valid .db file should pass the size check.
    Uses a temp directory to prevent overwriting the real resume.db.

    The endpoint hardcodes its DB path via Path(__file__) resolution,
    so we monkeypatch the backend_dir calculation to point to tmp_path.
    We also restore app.db.base engine after the test to prevent
    global state pollution.
    """
    import app.db.base as db_base
    import app.api.endpoints.import_data as import_module

    # Save original engine/session so we can restore after this test
    original_engine = db_base.engine
    original_session_local = db_base.SessionLocal

    # The endpoint calculates:
    #   backend_dir = Path(__file__).parent.parent.parent.parent.resolve()
    # where __file__ = backend/app/api/endpoints/import_data.py
    # Going up 4 levels: endpoints -> api -> app -> backend
    # So backend_dir = backend/
    # Then: db_path = backend_dir / "data" / "resume.db"
    #
    # We monkeypatch __file__ on the module so that
    # Path(fake_file).parent.parent.parent.parent.resolve() == tmp_path
    # fake_file must be 4 directory levels deep inside tmp_path.
    fake_file = str(tmp_path / "app" / "api" / "endpoints" / "import_data.py")
    monkeypatch.setattr(import_module, "__file__", fake_file)

    # Create the fake directory structure so the path resolution works
    (tmp_path / "app" / "api" / "endpoints").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data").mkdir(exist_ok=True)

    try:
        db_content = _make_minimal_sqlite_db()

        response = client.post(
            DB_IMPORT_URL,
            files={"file": ("small.db", io.BytesIO(db_content), "application/octet-stream")}
        )

        # Must NOT be 413 (size limit exceeded)
        assert response.status_code != 413, (
            f"Small 1KB file should NOT hit the 100MB size limit, got {response.status_code}"
        )
    finally:
        # Always restore the global engine to prevent test pollution
        db_base.engine = original_engine
        db_base.SessionLocal = original_session_local
