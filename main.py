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
    db_user = models.Users(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete('/user/{user_id}', response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    db.delete(db_user)
    db.commit()
    return db_user

@app.get('/savings/{user_id}', response_model=List[schemas.SavingResponse])
def get_savings(user_id: int, db: Session = Depends(get_db)):
    savings = db.query(models.Savings).filter(models.Savings.userid==user_id).all()
    return savings

@app.post('/add/saving/{user_id}', response_model=List[schemas.SavingResponse])
def add_savings(user_id: int, saving: List[schemas.SavingRequest], db: Session = Depends(get_db)):
    new_savings = []
    for item in saving:
        new_saving = models.Savings(userid=user_id, **item.model_dump())
        new_savings.append(new_saving)
    
    db.add_all(new_savings)
    db.commit()
    for item in new_savings:
        db.refresh(item)
    return new_savings

@app.patch('/edit/saving/', response_model=schemas.SavingResponse)
def edit_saving(user_id: int, saving_id: int, saving: schemas.EditSavingRequest, db: Session = Depends(get_db) ):
    saving_record = db.query(models.Savings)\
    .filter(models.Savings.userid==user_id)\
    .filter(models.Savings.id==saving_id)\
    .first()
    if not saving_record:
        raise HTTPException(status_code=404, detail="Record not found with id: {saving_id}")
    update_data = saving.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(saving_record, field, value)

    db.commit()
    db.refresh(saving_record)
    return saving_record

@app.delete('/delete/saving/', response_model=schemas.SavingResponse)
def delete_saving(user_id: int, saving_id: int, db: Session = Depends(get_db)):
    delete_record = db.query(models.Savings)\
    .filter(models.Savings.userid==user_id)\
    .filter(models.Savings.id==saving_id)\
    .first()
    if not delete_record:
        raise HTTPException(status_code=404, detail=f"Record not found with id: {saving_id}")
    db.delete(delete_record)
    db.commit()
    return delete_record