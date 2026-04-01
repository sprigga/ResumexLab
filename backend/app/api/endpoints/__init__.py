# Modified on 2026-04-01, Reason: Issue #9 — add missing module exports
from app.api.endpoints import (
    auth, personal_info, work_experience,
    education, certifications, languages,
    publications, github_projects, projects,
    import_data,
)

__all__ = [
    "auth",
    "personal_info",
    "work_experience",
    "education",
    "certifications",
    "languages",
    "publications",
    "github_projects",
    "projects",
    "import_data",
]
