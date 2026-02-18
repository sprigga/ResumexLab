"""
Tests for P0 Fix #1: Missing Authentication on Write Operations
CVSS 9.1 - Confirms all write endpoints require a valid JWT.

Each test checks:
  - Unauthenticated request → 401 Unauthorized
  - Or: Authenticated request → 2xx (success)
"""


# ── Education endpoints ──────────────────────────────────────────────────────

def test_create_education_requires_auth(client):
    """POST /education/ without token must return 401."""
    response = client.post("/api/education/", json={
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
    response = client.post("/api/education/", json={
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
    """POST /certifications/ with token must succeed."""
    response = client.post("/api/certifications/", json={
        "name_en": "AWS Solutions Architect", "display_order": 1
    }, headers=auth_headers)
    assert response.status_code in (200, 201), f"Expected 2xx, got {response.status_code}: {response.text}"


# ── Languages endpoints ──────────────────────────────────────────────────────

def test_create_language_requires_auth(client):
    """POST /languages/ without token must return 401."""
    response = client.post("/api/languages/", json={
        "language_en": "English", "proficiency_en": "Native", "display_order": 1
    })
    assert response.status_code == 401


# ── Publications endpoints ───────────────────────────────────────────────────

def test_create_publication_requires_auth(client):
    """POST /publications/ without token must return 401."""
    response = client.post("/api/publications/", json={
        "title": "Test Paper", "year": 2024, "display_order": 1
    })
    assert response.status_code == 401


# ── GitHub Projects endpoints ────────────────────────────────────────────────

def test_create_github_project_requires_auth(client):
    """POST /github-projects/ without token must return 401."""
    response = client.post("/api/github-projects/", json={
        "name_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401


# ── Work Experience endpoints ────────────────────────────────────────────────

def test_create_work_experience_requires_auth(client):
    """POST /work-experience/ without token must return 401."""
    response = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    })
    assert response.status_code == 401


def test_delete_work_experience_requires_auth(client, auth_headers):
    """DELETE /work-experience/{id} without token must return 401."""
    create_resp = client.post("/api/work-experience/", json={
        "company_en": "Test Corp", "position_en": "Engineer", "display_order": 1
    }, headers=auth_headers)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    exp_id = create_resp.json()["id"]

    response = client.delete(f"/api/work-experience/{exp_id}")
    assert response.status_code == 401


# ── Projects endpoints ───────────────────────────────────────────────────────

def test_create_project_requires_auth(client):
    """POST /projects/ without token must return 401."""
    response = client.post("/api/projects/", json={
        "title_en": "My Project", "display_order": 1
    })
    assert response.status_code == 401
