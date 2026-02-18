"""
Shared pytest fixtures for ResumeXLab backend tests.

Uses an in-memory SQLite database so tests never touch real data.
Overrides the get_db dependency so all endpoints use the test DB.
Uses StaticPool so all sessions share one in-memory DB connection.
"""
import pytest
import sys
import os
from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure the backend directory is on sys.path so `app.*` imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.db.base import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash, create_access_token

# Use in-memory SQLite with StaticPool so all sessions share one connection.
# Without StaticPool, each session opens a separate `:memory:` DB (empty).
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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
    try:
        yield db
    finally:
        db.rollback()
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
