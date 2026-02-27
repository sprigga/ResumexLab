# Remove Hardcoded Admin Credentials Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace hardcoded `admin` / `admin123` credentials in `init_db.py` with required environment variables that cause startup failure if not set.

**Architecture:** Add `ADMIN_USERNAME` and `ADMIN_PASSWORD` as required fields (no defaults) to `pydantic_settings.BaseSettings` in `config.py`. `init_db.py` reads from `settings`. If env vars are missing, pydantic raises `ValidationError` at import time and the app refuses to start.

**Tech Stack:** Python, FastAPI, pydantic-settings, pytest

---

### Task 1: Add required fields to `config.py`

**Files:**
- Modify: `backend/app/core/config.py`

**Step 1: Write the failing test**

Create `backend/tests/test_admin_credentials_config.py`:

```python
"""
Test that ADMIN_USERNAME and ADMIN_PASSWORD are read from environment variables.
"""
import os
import importlib
import pytest


def test_admin_username_read_from_env(monkeypatch):
    """Settings should expose ADMIN_USERNAME from environment."""
    monkeypatch.setenv("ADMIN_USERNAME", "myadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "supersecret")

    import app.core.config as config_module
    importlib.reload(config_module)

    assert config_module.settings.ADMIN_USERNAME == "myadmin"


def test_admin_password_read_from_env(monkeypatch):
    """Settings should expose ADMIN_PASSWORD from environment."""
    monkeypatch.setenv("ADMIN_USERNAME", "myadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "supersecret")

    import app.core.config as config_module
    importlib.reload(config_module)

    assert config_module.settings.ADMIN_PASSWORD == "supersecret"
```

**Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/test_admin_credentials_config.py -v
```

Expected: FAIL — `AttributeError: 'Settings' object has no attribute 'ADMIN_USERNAME'`

**Step 3: Add fields to `config.py`**

In `backend/app/core/config.py`, add after `ACCESS_TOKEN_EXPIRE_MINUTES`:

```python
# Admin user credentials (required - no defaults, must be set via environment)
ADMIN_USERNAME: str
ADMIN_PASSWORD: str
```

No default values — pydantic-settings will raise `ValidationError` at startup if these are not set.

**Step 4: Run test to verify it passes**

```bash
cd backend
pytest tests/test_admin_credentials_config.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add backend/app/core/config.py backend/tests/test_admin_credentials_config.py
git commit -m "feat: add required ADMIN_USERNAME and ADMIN_PASSWORD to settings"
```

---

### Task 2: Update `init_db.py` to use settings

**Files:**
- Modify: `backend/app/db/init_db.py`

**Step 1: Write the failing test**

Create `backend/tests/test_init_db.py`:

```python
"""
Test that init_db uses credentials from settings, not hardcoded values.
"""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.user import User


@pytest.fixture
def mem_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_init_db_uses_env_username(mem_db, monkeypatch):
    """init_db should create admin user with username from settings."""
    monkeypatch.setenv("ADMIN_USERNAME", "envadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "envpassword")

    import app.core.config as config_module
    import importlib
    importlib.reload(config_module)

    import app.db.init_db as init_db_module
    importlib.reload(init_db_module)

    init_db_module.init_db(mem_db)

    user = mem_db.query(User).filter(User.username == "envadmin").first()
    assert user is not None, "Admin user should be created with ADMIN_USERNAME from env"


def test_init_db_does_not_create_hardcoded_admin(mem_db, monkeypatch):
    """init_db must NOT create a user named 'admin' when ADMIN_USERNAME is different."""
    monkeypatch.setenv("ADMIN_USERNAME", "customadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "custompassword")

    import app.core.config as config_module
    import importlib
    importlib.reload(config_module)

    import app.db.init_db as init_db_module
    importlib.reload(init_db_module)

    init_db_module.init_db(mem_db)

    hardcoded_user = mem_db.query(User).filter(User.username == "admin").first()
    assert hardcoded_user is None, "Hardcoded 'admin' user must not be created"
```

**Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/test_init_db.py -v
```

Expected: FAIL — test finds `admin` user (hardcoded) instead of `envadmin`

**Step 3: Rewrite `init_db.py`**

Replace entire content of `backend/app/db/init_db.py`:

```python
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


def init_db(db: Session) -> None:
    """Initialize database with default admin user from environment variables."""

    user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not user:
        user = User(
            username=settings.ADMIN_USERNAME,
            email="admin@example.com",
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created admin user: {settings.ADMIN_USERNAME}")
    else:
        print(f"Admin user '{settings.ADMIN_USERNAME}' already exists")
```

**Step 4: Run test to verify it passes**

```bash
cd backend
pytest tests/test_init_db.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add backend/app/db/init_db.py backend/tests/test_init_db.py
git commit -m "feat: init_db reads admin credentials from settings, removes hardcoded values"
```

---

### Task 3: Update `.env` and `.env.example`

**Files:**
- Modify: `backend/.env`
- Modify: `backend/.env.example`

**Step 1: Add to `.env.example`**

Append to `backend/.env.example` after the `# Security` block:

```
# Admin User (required - no defaults, app will refuse to start if not set)
# Generate a strong password: python -c "import secrets; print(secrets.token_urlsafe(16))"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="change-this-before-deploying"
```

**Step 2: Add to `.env` (local development values)**

Append to `backend/.env`:

```
# Admin User
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin123"
```

Note: `.env` is not committed to git (verify `.gitignore`). This restores local dev convenience while keeping production safe.

**Step 3: Verify app starts correctly**

```bash
cd backend
python -c "from app.core.config import settings; print(settings.ADMIN_USERNAME)"
```

Expected output: `admin`

**Step 4: Verify app fails without env vars**

```bash
cd backend
ADMIN_USERNAME="" ADMIN_PASSWORD="" python -c "from app.core.config import settings"
```

Expected: `pydantic_settings.exceptions.SettingsError` or `ValidationError` — app refuses to start.

**Step 5: Run all tests**

```bash
cd backend
pytest tests/ -v
```

Expected: All tests PASS

**Step 6: Commit**

```bash
git add backend/.env.example
git commit -m "docs: add ADMIN_USERNAME and ADMIN_PASSWORD to .env.example"
```

Note: Do NOT commit `.env` — it should already be in `.gitignore`.

---

### Verification

After all tasks complete, verify the full fix:

```bash
# 1. Confirm no hardcoded credentials remain in init_db.py
grep -n "admin123\|\"admin\"" backend/app/db/init_db.py
# Expected: no output

# 2. Run full test suite
cd backend && pytest tests/ -v
# Expected: all PASS
```
