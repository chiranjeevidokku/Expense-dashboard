from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from typing import List
from income_api import models
from income_api import response_models
from database import get_db

income_router = APIRouter()

@cbv(income_router)
class Income:
    income_router.prefix = "/income"
    income_router.tags = ["/Income"]

    db: Session = Depends(get_db)

    @income_router.get('/{user_id}', response_model=List[response_models.IncomeResponse])
    def get_income(self, user_id: int):
        income = self.db.query(models.Income).filter(models.Income.userid==user_id).all()
        return income

    @income_router.post('/add', response_model=List[response_models.IncomeResponse])
    def add_income(self, user_id: int, income: List[response_models.IncomeRequest]):
        new_income = []
        for item in income:
            incoming = models.Income(userid=user_id, **item.model_dump())
            new_income.append(incoming)
        self.db.add_all(new_income)
        self.db.commit()
        for saved in new_income:
            self.db.refresh(saved)
        return new_income
    
    @income_router.patch('/edit', response_model=response_models.IncomeResponse)
    def edit_income(self, user_id: int, income_id: int, income: response_models.EditIncomeRequest):
        income_info = self.db.query(models.Income)\
            .filter(models.Income.userid==user_id)\
            .filter(models.Income.id==income_id)\
            .first()
        if not income_info:
            raise HTTPException(status_code=404, detail=f"Record not found with id: {income_id}")
        
        update_income = income.model_dump(exclude_unset=True)
        for key, value in update_income.items():
            setattr(income_info, key, value)
        
        self.db.commit()
        self.db.refresh(income_info)
        return income_info
    
    @income_router.delete('/delete', response_model=response_models.IncomeResponse)
    def delete_income(self, user_id: int, income_id: int, income: response_models.IncomeRequest):
        del_income = self.db.query(models.Income)\
            .filter(models.Income.id==income_id)\
            .filter(models.Income.userid==user_id)\
            .first()
        if not del_income:
            raise HTTPException(status_code=404, detail=f"Record not found with id: {income_id}")
        self.db.delete(del_income)
        self.db.commit()
        return del_income
        
        
        

