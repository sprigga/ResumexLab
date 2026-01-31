import sys
sys.path.insert(0, '/app')

from app.db.base import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT id, username, created_at FROM users'))
    users = result.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Created: {user[2]}")
