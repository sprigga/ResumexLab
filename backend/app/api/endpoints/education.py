"""
Education API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Refactored: 2026-02-27 - replaced repetitive CRUD with create_crud_router factory
"""

from app.api.crud_base import create_crud_router
from app.models.education import Education
from app.schemas.education import EducationCreate, EducationUpdate, EducationResponse

router = create_crud_router(
    model=Education,
    create_schema=EducationCreate,
    update_schema=EducationUpdate,
    response_schema=EducationResponse,
    not_found_detail="Education record not found",
)
