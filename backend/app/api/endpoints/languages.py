"""
Languages API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Refactored: 2026-02-27 - replaced repetitive CRUD with create_crud_router factory
"""

from app.api.crud_base import create_crud_router
from app.models.certification import Language
from app.schemas.certification import LanguageCreate, LanguageUpdate, LanguageResponse

router = create_crud_router(
    model=Language,
    create_schema=LanguageCreate,
    update_schema=LanguageUpdate,
    response_schema=LanguageResponse,
    not_found_detail="Language not found",
)
