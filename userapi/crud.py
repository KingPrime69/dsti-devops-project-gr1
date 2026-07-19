from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate, UserUpdate

def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalars(select(User).where(User.username == username)).first()

def list_users(db: Session, skip: int = 0, limit: int= 100) -> list[User]:
    return list(db.scalars(select(User).offset(skip).limit(limit)))

def create_user(db: Session, payload: UserCreate) -> User:
    user = User(username=payload.username, email=payload.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, payload: UserUpdate) -> User:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()