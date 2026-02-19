"""
Test that ADMIN_USERNAME and ADMIN_PASSWORD are read from environment variables.

Uses direct Settings() instantiation to avoid dependency on the module-level
settings singleton, which requires env vars at import time.
"""
import pytest
from pydantic import ValidationError
from app.core.config import Settings


def test_admin_username_read_from_env():
    """Settings should expose ADMIN_USERNAME passed as constructor argument."""
    s = Settings(ADMIN_USERNAME="myadmin", ADMIN_PASSWORD="supersecret")
    assert s.ADMIN_USERNAME == "myadmin"


def test_admin_password_read_from_env():
    """Settings should expose ADMIN_PASSWORD passed as constructor argument."""
    s = Settings(ADMIN_USERNAME="myadmin", ADMIN_PASSWORD="supersecret")
    assert s.ADMIN_PASSWORD == "supersecret"


def test_admin_username_is_str():
    """ADMIN_USERNAME must be a string (field type enforcement)."""
    s = Settings(ADMIN_USERNAME="testuser", ADMIN_PASSWORD="testpass")
    assert isinstance(s.ADMIN_USERNAME, str)


def test_admin_password_is_str():
    """ADMIN_PASSWORD must be a string (field type enforcement)."""
    s = Settings(ADMIN_USERNAME="testuser", ADMIN_PASSWORD="testpass")
    assert isinstance(s.ADMIN_PASSWORD, str)


def test_missing_admin_username_raises(monkeypatch):
    """Settings should raise ValidationError when ADMIN_USERNAME is missing."""
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    with pytest.raises(ValidationError):
        # _env_file=None prevents loading from .env so only ADMIN_PASSWORD is supplied
        Settings(ADMIN_PASSWORD="somepass", _env_file=None)


def test_missing_admin_password_raises(monkeypatch):
    """Settings should raise ValidationError when ADMIN_PASSWORD is missing."""
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    with pytest.raises(ValidationError):
        # _env_file=None prevents loading from .env so only ADMIN_USERNAME is supplied
        Settings(ADMIN_USERNAME="someuser", _env_file=None)
