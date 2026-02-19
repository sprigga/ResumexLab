"""
Test that ADMIN_USERNAME and ADMIN_PASSWORD are read from environment variables.
"""
from unittest.mock import patch
from app.core.config import settings


def test_admin_username_read_from_env():
    """Settings should expose ADMIN_USERNAME attribute."""
    with patch.object(settings, "ADMIN_USERNAME", "myadmin"):
        assert settings.ADMIN_USERNAME == "myadmin"


def test_admin_password_read_from_env():
    """Settings should expose ADMIN_PASSWORD attribute."""
    with patch.object(settings, "ADMIN_PASSWORD", "supersecret"):
        assert settings.ADMIN_PASSWORD == "supersecret"


def test_admin_username_is_str():
    """ADMIN_USERNAME must be a string (field type enforcement)."""
    assert isinstance(settings.ADMIN_USERNAME, str)


def test_admin_password_is_str():
    """ADMIN_PASSWORD must be a string (field type enforcement)."""
    assert isinstance(settings.ADMIN_PASSWORD, str)
