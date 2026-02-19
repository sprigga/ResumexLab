"""
Test that init_db uses credentials from settings, not hardcoded values.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.user import User
from app.core.config import Settings
from app.core.security import get_password_hash
from app.db.init_db import init_db


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
    """init_db should create admin user with ADMIN_USERNAME from settings."""
    monkeypatch.setenv("ADMIN_USERNAME", "envadmin")
    monkeypatch.setenv("ADMIN_PASSWORD", "envpassword")

    # Create a fresh Settings instance with the patched env vars
    test_settings = Settings(ADMIN_USERNAME="envadmin", ADMIN_PASSWORD="envpassword")

    # Patch the settings used by init_db
    import app.db.init_db as init_db_module
    monkeypatch.setattr(init_db_module, "settings", test_settings)

    init_db(mem_db)

    user = mem_db.query(User).filter(User.username == "envadmin").first()
    assert user is not None, "Admin user should be created with ADMIN_USERNAME from env"


def test_init_db_does_not_create_hardcoded_admin(mem_db, monkeypatch):
    """init_db must NOT create a user named 'admin' when ADMIN_USERNAME is different."""
    test_settings = Settings(ADMIN_USERNAME="customadmin", ADMIN_PASSWORD="custompassword")

    import app.db.init_db as init_db_module
    monkeypatch.setattr(init_db_module, "settings", test_settings)

    init_db(mem_db)

    hardcoded_user = mem_db.query(User).filter(User.username == "admin").first()
    assert hardcoded_user is None, "Hardcoded 'admin' user must not be created"


def test_init_db_does_not_duplicate_user(mem_db, monkeypatch):
    """Calling init_db twice should not create duplicate users."""
    test_settings = Settings(ADMIN_USERNAME="admin", ADMIN_PASSWORD="secret")

    import app.db.init_db as init_db_module
    monkeypatch.setattr(init_db_module, "settings", test_settings)

    init_db(mem_db)
    init_db(mem_db)  # second call

    count = mem_db.query(User).filter(User.username == "admin").count()
    assert count == 1, "init_db called twice should not duplicate admin user"
