"""
Tests for P0 Fix #2: File Upload DoS Vulnerability
CVSS 7.5 - Confirms the database import endpoint rejects oversized files
before reading them into memory.

MAX_DB_FILE_SIZE = 100MB (set in import_data.py)
"""
import io
import sqlite3
import tempfile
import os


DB_IMPORT_URL = "/api/import/database/import/"


def _make_minimal_sqlite_db() -> bytes:
    """
    Create a minimal valid SQLite database in memory and return its bytes.
    Using a real SQLite file prevents the endpoint from corrupting the
    on-disk resume.db with garbage bytes, which would break subsequent
    pytest sessions (app/main.py calls create_all at import time).
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        conn = sqlite3.connect(tmp_path)
        conn.close()
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        os.unlink(tmp_path)


def test_non_db_file_rejected(client):
    """
    A file that doesn't end in .db must be rejected with 400.
    This is checked BEFORE reading file content (fastest rejection).
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
    Note: generating 101MB in memory is intentional for this one-time verification.
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


def test_small_db_file_passes_size_check(client):
    """
    A small valid .db file must pass the size check and must NOT be rejected with 413.
    A genuine SQLite file is used so that if the endpoint writes it to disk, the
    on-disk resume.db remains a valid SQLite file and does not break subsequent
    pytest sessions.
    The endpoint returns 200 on success or 500 on any DB validation error.
    The critical assertion is that the 100MB size guard does NOT fire.
    """
    small_db_bytes = _make_minimal_sqlite_db()

    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("small.db", io.BytesIO(small_db_bytes), "application/octet-stream")}
    )
    # The only forbidden response is 413 (Request Entity Too Large).
    # A small valid SQLite file must never trigger the 100MB size limit.
    assert response.status_code != 413, (
        f"Small valid .db file should NOT hit the 100MB size limit, got {response.status_code}"
    )
    # 200: endpoint accepted and wrote the file successfully.
    # 400: endpoint rejected for format reasons (unexpected but allowed).
    # 500: DB validation step failed (acceptable — size check was not the cause).
    assert response.status_code in (200, 400, 500), (
        f"Unexpected status code for small valid .db file: "
        f"{response.status_code}: {response.text}"
    )
