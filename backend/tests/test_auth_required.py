"""
Tests for P0 Fix #1: Missing Authentication on Write Operations
CVSS 9.1 - Confirms all write endpoints require a valid JWT.

Each endpoint pair:
  - requires_auth: Unauthenticated request → 401 Unauthorized
  - with_auth: Authenticated request → 2xx + verifies resource created
"""


# ── Education endpoints ──────────────────────────────────────────────────────

def test_create_education_requires_auth(client):
    """POST /education/ without token must return 401."""
    response = client.post("/api/education/", json={
        "school_zh": "測試大學",
        "school_en": "Test University",
        "display_order": 1
    })
    assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"


def test_create_education_with_auth(client, auth_headers):
    """POST /education/ with valid token must succeed and return a resource with an ID."""
    response = client.post("/api/education/", json={
        "school_zh": "測試大學",
        "school_en": "Test University",
        "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["school_en"] == "Test University"


def test_update_education_requires_auth(client, auth_headers):
    """PUT /education/{id} without token must return 401."""
    create_resp = client.post("/api/education/", json={
        "school_en": "Test University", "display_order": 1
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    education_id = create_resp.json()["id"]

    response = client.put(f"/api/education/{education_id}", json={"school_en": "Changed"})
    assert response.status_code == 401


def test_delete_education_requires_auth(client, auth_headers):
    """DELETE /education/{id} without token must return 401."""
    create_resp = client.post("/api/education/", json={
        "school_en": "Test University", "display_order": 1
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    education_id = create_resp.json()["id"]

    response = client.delete(f"/api/education/{education_id}")
    assert response.status_code == 401


# ── Certifications endpoints ─────────────────────────────────────────────────

def test_create_certification_requires_auth(client):
    """POST /certifications/ without token must return 401."""
    response = client.post("/api/certifications/", json={
        "name_en": "AWS Solutions Architect", "display_order": 1
    })
    assert response.status_code == 401


def test_create_certification_with_auth(client, auth_headers):
    """POST /certifications/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/certifications/", json={
        "name_en": "AWS Solutions Architect", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["name_en"] == "AWS Solutions Architect"


# ── Languages endpoints ──────────────────────────────────────────────────────

def test_create_language_requires_auth(client):
    """POST /languages/ without token must return 401."""
    response = client.post("/api/languages/", json={
        "language_en": "English", "proficiency_en": "Native", "display_order": 1
    })
    assert response.status_code == 401


def test_create_language_with_auth(client, auth_headers):
    """POST /languages/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/languages/", json={
        "language_en": "English", "proficiency_en": "Native", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["language_en"] == "English"


# ── Publications endpoints ───────────────────────────────────────────────────

def test_create_publication_requires_auth(client):
    """POST /publications/ without token must return 401."""
    response = client.post("/api/publications/", json={
        "title": "Test Paper", "year": 2024, "display_order": 1
    })
    assert response.status_code == 401


def test_create_publication_with_auth(client, auth_headers):
    """POST /publications/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/publications/", json={
        "title": "Test Paper", "year": 2024, "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["title"] == "Test Paper"


# ── GitHub Projects endpoints ────────────────────────────────────────────────

def test_create_github_project_requires_auth(client):
    """POST /github-projects/ without token must return 401."""
    response = client.post("/api/github-projects/", json={
        "name_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401


def test_create_github_project_with_auth(client, auth_headers):
    """POST /github-projects/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/github-projects/", json={
        "name_en": "My Project", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["name_en"] == "My Project"


# ── Work Experience endpoints ────────────────────────────────────────────────

def test_create_work_experience_requires_auth(client):
    """POST /work-experience/ without token must return 401."""
    response = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    })
    assert response.status_code == 401


def test_create_work_experience_with_auth(client, auth_headers):
    """POST /work-experience/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["company_en"] == "Test Corp"


def test_delete_work_experience_requires_auth(client, auth_headers):
    """DELETE /work-experience/{id} without token must return 401."""
    create_resp = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    exp_id = create_resp.json()["id"]

    response = client.delete(f"/api/work-experience/{exp_id}")
    assert response.status_code == 401


def test_delete_work_experience_with_auth(client, auth_headers):
    """DELETE /work-experience/{id} with token must succeed (204 No Content)."""
    create_resp = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    exp_id = create_resp.json()["id"]

    response = client.delete(f"/api/work-experience/{exp_id}", headers=auth_headers)
    assert response.status_code == 204, f"Expected 204, got {response.status_code}: {response.text}"


# ── Projects endpoints ───────────────────────────────────────────────────────

def test_create_project_requires_auth(client):
    """POST /projects/ without token must return 401."""
    response = client.post("/api/projects/", json={
        "title_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401


def test_create_project_with_auth(client, auth_headers):
    """POST /projects/ with token must succeed and return a resource with an ID."""
    response = client.post("/api/projects/", json={
        "title_en": "My Project", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"
    data = response.json()
    assert "id" in data, f"Response body missing 'id': {data}"
    assert data["title_en"] == "My Project"


# ── Expired token test ───────────────────────────────────────────────────────

def test_expired_token_rejected(client, db_session):
    """
    A JWT that expired in the past must be rejected with 401.
    This verifies the token validation logic in get_current_user.
    """
    from app.core.security import create_access_token, get_password_hash
    from app.models.user import User
    from datetime import timedelta

    # Create user directly in test DB
    user = User(username="expireduser", password_hash=get_password_hash("pw"), email="e@e.com")
    db_session.add(user)
    db_session.commit()

    # Create an already-expired token (negative timedelta = expired immediately)
    expired_token = create_access_token(
        data={"sub": "expireduser"},
        expires_delta=timedelta(seconds=-1)
    )
    headers = {"Authorization": f"Bearer {expired_token}"}

    response = client.post("/api/education/", json={
        "school_en": "Test", "display_order": 1
    }, headers=headers)
    assert response.status_code == 401, f"Expired token should be rejected, got {response.status_code}"
