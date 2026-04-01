"""
Generic CRUD router factory for standard endpoints.
Author: Polo (林鴻全)
Date: 2026-02-27

Creates a complete CRUD APIRouter (GET /, GET /{id}, POST /, PUT /{id}, DELETE /{id})
for any SQLAlchemy model + Pydantic schema combination.
"""

from typing import Type, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.base import get_db
from app.api.endpoints.auth import get_current_user
from app.models.user import User


def create_crud_router(
    model,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    response_schema: Type[BaseModel],
    not_found_detail: str = "Record not found",
    order_by_field: str = "display_order",
    entity_name: str = "Record",
) -> APIRouter:
    """
    Factory that returns an APIRouter with standard CRUD endpoints.

    Args:
        model: SQLAlchemy model class
        create_schema: Pydantic schema for POST body
        update_schema: Pydantic schema for PUT body
        response_schema: Pydantic schema for responses
        not_found_detail: Error message for 404 responses
        order_by_field: Model attribute name to sort list results by
        entity_name: Human-readable name used in success messages
    """
    router = APIRouter()

    @router.get("/", response_model=List[response_schema])
    def get_all(db: Session = Depends(get_db)):
        return db.query(model).order_by(getattr(model, order_by_field)).all()

    # Modified on 2026-04-01, Reason: Issue #8 — standardize status codes
    @router.get("/{item_id}", response_model=response_schema)
    def get_one(item_id: int, db: Session = Depends(get_db)):
        item = db.query(model).filter(model.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
        return item

    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    @router.post("/", response_model=response_schema)
    def create(
        item_data: create_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = model(**item_data.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    @router.put("/{item_id}", response_model=response_schema)
    def update(
        item_id: int,
        item_data: update_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = db.query(model).filter(model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
            for key, value in item_data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

    # Modified on 2026-04-01, Reason: Issue #5 — add transaction rollback
    @router.delete("/{item_id}")
    def delete(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            db_item = db.query(model).filter(model.id == item_id).first()
            if not db_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found_detail)
            db.delete(db_item)
            db.commit()
            return {"message": f"{entity_name} deleted successfully"}
        except HTTPException:
            raise
        except Exception:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

    return router
