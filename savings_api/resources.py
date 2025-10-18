from fastapi import Depends, HTTPException, APIRouter
from savings_api import response_models
from savings_api import models
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv


savings_router = APIRouter()

@cbv(savings_router)
class Savings:
    savings_router.prefix = "/savings"
    savings_router.tags = ["/Savings"]

    db: Session = Depends(get_db)

    @savings_router.get('/{user_id}', response_model=List[response_models.SavingResponse])
    def get_savings(self, user_id: int, ):
        savings = self.db.query(models.Savings).filter(models.Savings.userid==user_id).all()
        return savings

    @savings_router.post('/add/{user_id}', response_model=List[response_models.SavingResponse])
    def add_savings(self, user_id: int, saving: List[response_models.SavingRequest]):
        new_savings = []
        for item in saving:
            new_saving = models.Savings(userid=user_id, **item.model_dump())
            new_savings.append(new_saving)
        
        self.db.add_all(new_savings)
        self.db.commit()
        for item in new_savings:
            self.db.refresh(item)
        return new_savings

    @savings_router.patch('/edit', response_model=response_models.SavingResponse)
    def edit_saving(self, user_id: int, saving_id: int, saving: response_models.EditSavingRequest):
        saving_record = self.db.query(models.Savings)\
        .filter(models.Savings.userid==user_id)\
        .filter(models.Savings.id==saving_id)\
        .first()
        if not saving_record:
            raise HTTPException(status_code=404, detail="Record not found with id: {saving_id}")
        update_data = saving.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(saving_record, field, value)

        self.db.commit()
        self.db.refresh(saving_record)
        return saving_record

    @savings_router.delete('/delete', response_model=response_models.SavingResponse)
    def delete_saving(self, user_id: int, saving_id: int):
        delete_record = self.db.query(models.Savings)\
        .filter(models.Savings.userid==user_id)\
        .filter(models.Savings.id==saving_id)\
        .first()
        if not delete_record:
            raise HTTPException(status_code=404, detail=f"Record not found with id: {saving_id}")
        self.db.delete(delete_record)
        self.db.commit()
        return delete_record
