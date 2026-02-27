"""
Publications API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Refactored: 2026-02-27 - replaced repetitive CRUD with create_crud_router factory
"""

from app.api.crud_base import create_crud_router
from app.models.publication import Publication
from app.schemas.publication import PublicationCreate, PublicationUpdate, PublicationResponse

router = create_crud_router(
    model=Publication,
    create_schema=PublicationCreate,
    update_schema=PublicationUpdate,
    response_schema=PublicationResponse,
    not_found_detail="Publication not found",
)
