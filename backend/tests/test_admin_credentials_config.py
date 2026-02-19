"""
Test that ADMIN_USERNAME and ADMIN_PASSWORD are read from environment variables.
"""
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
