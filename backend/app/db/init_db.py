from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User


def init_db(db: Session) -> None:
    """Initialize database with default admin user"""

    # Check if admin user exists
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123")  # Default password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print("Created default admin user: admin / admin123")
    else:
        print("Admin user already exists")
