from app.db.base import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT id, username, created_at FROM users'))
    users = [dict(row) for row in result]
    print("Users in database:", users)
