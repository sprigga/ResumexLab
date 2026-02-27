"""
GitHub Projects API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Refactored: 2026-02-27 - replaced repetitive CRUD with create_crud_router factory
"""

from app.api.crud_base import create_crud_router
from app.models.publication import GithubProject
from app.schemas.publication import GithubProjectCreate, GithubProjectUpdate, GithubProjectResponse

router = create_crud_router(
    model=GithubProject,
    create_schema=GithubProjectCreate,
    update_schema=GithubProjectUpdate,
    response_schema=GithubProjectResponse,
    not_found_detail="GitHub project not found",
)
