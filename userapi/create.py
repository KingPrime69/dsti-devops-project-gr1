from database import SessionLocal
from schemas import UserCreate
import crud

db = SessionLocal()
u = crud.create_user(db, UserCreate(username='quentin', email='q@example.com'))
print(u.id, u.username, u.created_at)
print(crud.list_users(db))
db.close()