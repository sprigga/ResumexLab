from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models.personal_info import PersonalInfo
from app.schemas.personal_info import PersonalInfoInDB, PersonalInfoCreate, PersonalInfoUpdate
from app.api.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=PersonalInfoInDB)
async def get_personal_info(db: Session = Depends(get_db)):
    """Get personal information (public endpoint)

    已修改於 2025-01-12，原因：當沒有個人資訊時，回傳預設空物件而不是 404 錯誤
    這樣可以避免前端顯示 "No resume data available" 訊息
    """
    info = db.query(PersonalInfo).first()
    if not info:
        # 回傳預設的空物件結構，讓前端可以正常渲染
        return PersonalInfoInDB(
            id=0,
            name_zh="",
            name_en="",
            phone="",
            email="",
            address_zh="",
            address_en="",
            objective_zh="",
            objective_en="",
            personality_zh="",
            personality_en="",
            summary_zh="",
            summary_en="",
            created_at=None,
            updated_at=None
        )
    return info


@router.post("/", response_model=PersonalInfoInDB)
async def create_personal_info(
    info_data: PersonalInfoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create personal information (requires authentication)"""
    # Check if personal info already exists
    existing_info = db.query(PersonalInfo).first()
    if existing_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal information already exists. Use PUT to update."
        )

    db_info = PersonalInfo(**info_data.model_dump())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info


@router.put("/", response_model=PersonalInfoInDB)
async def update_personal_info(
    info_data: PersonalInfoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update personal information (requires authentication)"""
    info = db.query(PersonalInfo).first()

    if not info:
        # Create new if doesn't exist
        info = PersonalInfo(**info_data.model_dump())
        db.add(info)
    else:
        # Update existing
        update_data = info_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(info, field, value)

    db.commit()
    db.refresh(info)
    return info
