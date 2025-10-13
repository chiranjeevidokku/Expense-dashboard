from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

app = FastAPI()

@app.get('/')
def info():
    return 'Fast APi is started'


@app.get("/users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/user", response_model=schemas.UserResponse)
def add_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    print("Payload Info***", user)
    db_user = models.Users(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete('/user/{user_id}', response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    print("User deleted", user_id)
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    db.delete(db_user)
    db.commit()
    return db_user