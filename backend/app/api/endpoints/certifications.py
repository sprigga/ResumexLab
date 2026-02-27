"""
Certifications API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
Refactored: 2026-02-27 - replaced repetitive CRUD with create_crud_router factory
"""

from app.api.crud_base import create_crud_router
from app.models.certification import Certification
from app.schemas.certification import CertificationCreate, CertificationUpdate, CertificationResponse

router = create_crud_router(
    model=Certification,
    create_schema=CertificationCreate,
    update_schema=CertificationUpdate,
    response_schema=CertificationResponse,
    not_found_detail="Certification not found",
)
