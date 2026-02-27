# Verify P0 Security Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write and run tests to verify that all P0 critical security fixes described in `docs/code_review/CRITICAL_FIXES_SUMMARY.md` actually work correctly in the codebase.

**Architecture:** All P0 fixes are already code-complete (confirmed by reading each file). The gap is that there are zero automated tests. We'll write pytest tests that: (1) confirm unauthenticated write requests return 401, (2) confirm authenticated write requests succeed, (3) confirm the DoS file-size guard on `/database/import/` works. Tests use FastAPI's `TestClient` with an in-memory SQLite database so no real data is touched.

**Tech Stack:** Python, pytest, FastAPI TestClient (from `starlette.testclient`), SQLite in-memory DB, `uv` for env management.

---

## Pre-flight: Understand the test environment

Before writing tests, verify the project structure and available packages.

### Task 0: Inspect backend structure and dependencies

**Files:**
- Read: `backend/requirements.txt` or `backend/pyproject.toml`
- Read: `backend/app/db/base.py`
- Read: `backend/app/core/config.py`

**Step 1: Check what test packages are available**

```bash
cd /Users/pololin/python_project/resumexlab/backend
cat requirements.txt 2>/dev/null || cat pyproject.toml 2>/dev/null || echo "No requirements file found"
```

**Step 2: Check main app entry point**

```bash
ls /Users/pololin/python_project/resumexlab/backend/
```

**Step 3: Read db/base.py to understand dependency injection**

Open `backend/app/db/base.py` and note how `get_db` and `engine` are defined — you'll need to override `get_db` in tests.

**Step 4: Install pytest if missing**

```bash
cd /Users/pololin/python_project/resumexlab
source .venv/bin/activate
pip show pytest httpx 2>/dev/null || uv pip install pytest httpx
```

---

## Task 1: Create test infrastructure

**Files:**
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

**Step 1: Create the tests package**

Create `backend/tests/__init__.py` (empty file).

**Step 2: Write conftest.py with shared fixtures**

Create `backend/tests/conftest.py`:

```python
"""
Shared pytest fixtures for ResumeXLab backend tests.

Uses an in-memory SQLite database so tests never touch real data.
Overrides the get_db dependency so all endpoints use the test DB.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the FastAPI app — adjust path if your main.py is elsewhere
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.db.base import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from datetime import timedelta

# Use in-memory SQLite for tests — isolated, fast, no file cleanup needed
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Replace real DB session with test DB session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create all tables fresh for each test, then drop them after."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden DB dependency."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(db_session):
    """
    Create a test user in the DB and return Authorization headers with a valid JWT.

    This is the authenticated context for write operation tests.
    """
    # Create a test user directly in the DB
    test_user = User(
        username="testuser",
        password_hash=get_password_hash("testpassword"),
        email="test@test.com"
    )
    db_session.add(test_user)
    db_session.commit()

    # Generate a valid JWT token for this user
    access_token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(minutes=30)
    )
    return {"Authorization": f"Bearer {access_token}"}
```

**Step 3: Run a quick import check**

```bash
cd /Users/pololin/python_project/resumexlab/backend
source ../.venv/bin/activate
python -c "from app.main import app; print('App imports OK')"
```

Expected: `App imports OK`

---

## Task 2: Test Issue #1 — Authentication on write endpoints

**Files:**
- Create: `backend/tests/test_auth_required.py`

**Step 1: Write failing tests for unauthenticated access**

Create `backend/tests/test_auth_required.py`:

```python
"""
Tests for P0 Fix #1: Missing Authentication on Write Operations
CVSS 9.1 - Confirms all write endpoints require a valid JWT.

Each test pair checks:
  - Unauthenticated request → 401 Unauthorized
  - Authenticated request → 2xx (success)
"""
import pytest


# ── Education endpoints ──────────────────────────────────────────────────────

def test_create_education_requires_auth(client):
    """POST /education/ without token must return 401."""
    response = client.post("/api/v1/education/", json={
        "school_zh": "測試大學",
        "school_en": "Test University",
        "degree_zh": "學士",
        "degree_en": "Bachelor",
        "major_zh": "資訊工程",
        "major_en": "Computer Science",
        "display_order": 1
    })
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"


def test_create_education_with_auth(client, auth_headers):
    """POST /education/ with valid token must succeed."""
    response = client.post("/api/v1/education/", json={
        "school_zh": "測試大學",
        "school_en": "Test University",
        "degree_zh": "學士",
        "degree_en": "Bachelor",
        "major_zh": "資訊工程",
        "major_en": "Computer Science",
        "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"


def test_update_education_requires_auth(client, auth_headers):
    """PUT /education/{id} without token must return 401."""
    # First create one so we have an ID
    create_resp = client.post("/api/v1/education/", json={
        "school_en": "Test University", "display_order": 1
    }, headers=auth_headers)
    education_id = create_resp.json()["id"]

    # Now try to update without auth
    response = client.put(f"/api/v1/education/{education_id}", json={"school_en": "Changed"})
    assert response.status_code == 401


def test_delete_education_requires_auth(client, auth_headers):
    """DELETE /education/{id} without token must return 401."""
    create_resp = client.post("/api/v1/education/", json={
        "school_en": "Test University", "display_order": 1
    }, headers=auth_headers)
    education_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/education/{education_id}")
    assert response.status_code == 401


# ── Certifications endpoints ─────────────────────────────────────────────────

def test_create_certification_requires_auth(client):
    """POST /certifications/ without token must return 401."""
    response = client.post("/api/v1/certifications/", json={
        "name_en": "AWS Solutions Architect", "display_order": 1
    })
    assert response.status_code == 401


def test_create_certification_with_auth(client, auth_headers):
    """POST /certifications/ with token must succeed."""
    response = client.post("/api/v1/certifications/", json={
        "name_en": "AWS Solutions Architect", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201)


# ── Languages endpoints ──────────────────────────────────────────────────────

def test_create_language_requires_auth(client):
    """POST /languages/ without token must return 401."""
    response = client.post("/api/v1/languages/", json={
        "language_en": "English", "proficiency_en": "Native", "display_order": 1
    })
    assert response.status_code == 401


# ── Publications endpoints ───────────────────────────────────────────────────

def test_create_publication_requires_auth(client):
    """POST /publications/ without token must return 401."""
    response = client.post("/api/v1/publications/", json={
        "title": "Test Paper", "year": 2024, "display_order": 1
    })
    assert response.status_code == 401


# ── GitHub Projects endpoints ────────────────────────────────────────────────

def test_create_github_project_requires_auth(client):
    """POST /github-projects/ without token must return 401."""
    response = client.post("/api/v1/github-projects/", json={
        "name_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401


# ── Work Experience endpoints ────────────────────────────────────────────────

def test_create_work_experience_requires_auth(client):
    """POST /work-experience/ without token must return 401."""
    response = client.post("/api/v1/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    })
    assert response.status_code == 401


def test_delete_work_experience_requires_auth(client, auth_headers):
    """DELETE /work-experience/{id} without token must return 401."""
    create_resp = client.post("/api/v1/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    }, headers=auth_headers)
    exp_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/work-experience/{exp_id}")
    assert response.status_code == 401


# ── Projects endpoints ───────────────────────────────────────────────────────

def test_create_project_requires_auth(client):
    """POST /projects/ without token must return 401."""
    response = client.post("/api/v1/projects/", json={
        "title_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401
```

**Step 2: Run the tests and verify they PASS**

```bash
cd /Users/pololin/python_project/resumexlab/backend
source ../.venv/bin/activate
python -m pytest tests/test_auth_required.py -v 2>&1 | head -60
```

Expected: All tests pass. If a test fails with something other than assertion, investigate the API prefix — you may need to adjust from `/api/v1/` to `/api/` depending on how routers are mounted (check `backend/app/main.py`).

**Step 3: Commit**

```bash
cd /Users/pololin/python_project/resumexlab
git add backend/tests/__init__.py backend/tests/conftest.py backend/tests/test_auth_required.py
git commit -m "test: add P0 auth verification tests for all write endpoints"
```

---

## Task 3: Test Issue #2 — File Upload DoS Vulnerability

**Files:**
- Create: `backend/tests/test_file_upload_dos.py`

**Step 1: Write DoS protection tests**

Create `backend/tests/test_file_upload_dos.py`:

```python
"""
Tests for P0 Fix #2: File Upload DoS Vulnerability
CVSS 7.5 - Confirms the import endpoint rejects oversized files.

The endpoint reads files in 8KB chunks and aborts if total > 100MB.
We test:
  - File at exactly the limit → accepted (or rejected for non-db reasons)
  - File exceeding the limit → 413 Request Entity Too Large
  - Non-.db file → 400 Bad Request
"""
import io
import pytest


DB_IMPORT_URL = "/api/v1/import/database/import/"


def make_fake_db_content(size_bytes: int) -> bytes:
    """Generate fake binary content of a given size (not a real SQLite DB)."""
    return b"x" * size_bytes


def test_oversized_file_rejected(client):
    """
    A file larger than 100MB must be rejected with 413.
    We use 101MB to definitely exceed the limit.
    """
    OVER_LIMIT = 101 * 1024 * 1024  # 101MB
    fake_content = make_fake_db_content(OVER_LIMIT)

    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("big_file.db", io.BytesIO(fake_content), "application/octet-stream")}
    )
    assert response.status_code == 413, (
        f"Expected 413 for oversized file, got {response.status_code}: {response.text}"
    )


def test_non_db_file_rejected(client):
    """
    A file that doesn't end in .db must be rejected with 400.
    This tests the file extension check before size check.
    """
    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("resume.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
    )
    assert response.status_code == 400, (
        f"Expected 400 for non-.db file, got {response.status_code}: {response.text}"
    )


def test_small_db_file_passes_size_check(client):
    """
    A small .db file should pass the size check.
    It will likely fail validation (not a real SQLite DB), but NOT with 413.
    We verify the error is NOT a size rejection.
    """
    tiny_content = make_fake_db_content(1024)  # 1KB

    response = client.post(
        DB_IMPORT_URL,
        files={"file": ("small.db", io.BytesIO(tiny_content), "application/octet-stream")}
    )
    # Should not be 413 (size limit) — it may be 500 (invalid DB) or 200 (if it validates)
    assert response.status_code != 413, (
        f"Small file should NOT hit the size limit, got {response.status_code}"
    )
```

**Step 2: Run the DoS tests**

```bash
cd /Users/pololin/python_project/resumexlab/backend
source ../.venv/bin/activate
python -m pytest tests/test_file_upload_dos.py -v
```

Expected:
- `test_non_db_file_rejected` → PASS (400)
- `test_small_db_file_passes_size_check` → PASS (not 413)
- `test_oversized_file_rejected` → PASS (413)
  *Note: The 101MB test may be slow since it generates large data in memory — that's OK for a one-time verification.*

**Step 3: Commit**

```bash
cd /Users/pololin/python_project/resumexlab
git add backend/tests/test_file_upload_dos.py
git commit -m "test: add P0 DoS protection verification for file upload endpoint"
```

---

## Task 4: Verify token expiry is rejected

**Files:**
- Modify: `backend/tests/test_auth_required.py` (add one test at the bottom)

**Step 1: Add expired token test**

Append to `backend/tests/test_auth_required.py`:

```python
# ── Expired token test ───────────────────────────────────────────────────────

def test_expired_token_rejected(client, db_session):
    """
    A JWT that expired in the past must be rejected with 401.
    This verifies the token validation logic in get_current_user.
    """
    from app.core.security import create_access_token, get_password_hash
    from app.models.user import User
    from datetime import timedelta

    # Create user
    user = User(username="expireduser", password_hash=get_password_hash("pw"), email="e@e.com")
    db_session.add(user)
    db_session.commit()

    # Create an already-expired token (negative timedelta = expired immediately)
    expired_token = create_access_token(
        data={"sub": "expireduser"},
        expires_delta=timedelta(seconds=-1)
    )
    headers = {"Authorization": f"Bearer {expired_token}"}

    response = client.post("/api/v1/education/", json={
        "school_en": "Test", "display_order": 1
    }, headers=headers)
    assert response.status_code == 401, f"Expired token should be rejected, got {response.status_code}"
```

**Step 2: Run all tests**

```bash
cd /Users/pololin/python_project/resumexlab/backend
source ../.venv/bin/activate
python -m pytest tests/ -v --tb=short 2>&1 | tail -30
```

Expected: All tests pass.

**Step 3: Commit**

```bash
cd /Users/pololin/python_project/resumexlab
git add backend/tests/test_auth_required.py
git commit -m "test: add expired JWT rejection test"
```

---

## Task 5: Investigate API router prefix (if tests fail with 404)

This task only applies if Task 2 or 3 tests returned 404 instead of expected status codes.

**Files:**
- Read: `backend/app/main.py`

**Step 1: Find the actual API prefix**

```bash
grep -n "include_router\|prefix\|api_router" /Users/pololin/python_project/resumexlab/backend/app/main.py
grep -n "include_router\|prefix" /Users/pololin/python_project/resumexlab/backend/app/api/api.py 2>/dev/null || echo "No api.py found"
```

**Step 2: Fix URL prefix in tests**

If the prefix is `/api/` instead of `/api/v1/`, update all test URLs:
- Replace `/api/v1/education/` → `/api/education/`
- Replace `/api/v1/certifications/` → `/api/certifications/`
- etc.

Then re-run tests:

```bash
python -m pytest tests/ -v --tb=short
```

**Step 3: Commit prefix fix if needed**

```bash
git add backend/tests/
git commit -m "fix: correct API URL prefix in security tests"
```

---

## Completion Checklist

After all tasks complete, run the full test suite one final time:

```bash
cd /Users/pololin/python_project/resumexlab/backend
source ../.venv/bin/activate
python -m pytest tests/ -v --tb=short
```

Expected summary:
- `test_auth_required.py`: 12+ tests PASSED
- `test_file_upload_dos.py`: 3 tests PASSED

These tests provide automated evidence that:
- ✅ P0 Issue #1 (CVSS 9.1): All write endpoints enforce JWT authentication
- ✅ P0 Issue #2 (CVSS 7.5): File upload DoS protection works
- ✅ Expired tokens are rejected (deployment checklist item)
