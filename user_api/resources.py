from typing import List
from user_api import reponse_models
from fastapi import Depends, HTTPException, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from user_api import models as ums
from fastapi_utils.cbv import cbv

user_router = APIRouter()

@cbv(user_router)
class Users:

    user_router.prefix = "/users"
    user_router.tags = ["Users"]
    db: Session = Depends(get_db)

    @user_router.get("/", response_model=List[reponse_models.User])
    def get_users(self):
        return self.db.query(ums.Users).all()

    @user_router.post("/add_user", response_model=reponse_models.UserResponse)
    def add_user(self, user: reponse_models.CreateUser):
        db_user = ums.Users(name=user.name)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    @user_router.delete('/del_user/{user_id}', response_model=reponse_models.UserResponse)
    def delete_user(self, user_id: int):
        db_user = self.db.query(ums.Users).filter(ums.Users.id == user_id).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found!")
        
        self.db.delete(db_user)
        self.db.commit()
        return db_user