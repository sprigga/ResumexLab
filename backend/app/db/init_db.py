from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


def init_db(db: Session) -> None:
    """Initialize database with admin user credentials from environment variables."""

    user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not user:
        user = User(
            username=settings.ADMIN_USERNAME,
            email="admin@example.com",
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created admin user: {settings.ADMIN_USERNAME}")
    else:
        print(f"Admin user '{settings.ADMIN_USERNAME}' already exists")
