from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models
from database import Base, engine, get_db
from schemas import UserCreate, UserOut, UserUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", version="1.0.0")

@app.get("/health")
def health(response: Response, db: Session = Depends(get_db)):
    try: 
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy"}

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "username or email already exists")

@app.get("/users", response_model=list[UserOut])
def list_users(skip: int=0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user

@app.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    try:
        return crud.update_user(db, user, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "username or email already exists")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    crud.delete_user(db, user)

