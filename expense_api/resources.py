from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv
from typing import List
from expense_api import models
from expense_api import response_models
from database import get_db

expense_router = APIRouter()

@cbv(expense_router)
class Income:
    expense_router.prefix = "/expense"
    expense_router.tags = ["/Expense"]

    db: Session = Depends(get_db)

    @expense_router.get('/{user_id}', response_model=List[response_models.ExpenseResponse])
    def get_expense(self, user_id: int):
        income = self.db.query(models.Expenditure).filter(models.Expenditure.userid==user_id).all()
        return income

    @expense_router.post('/add', response_model=List[response_models.ExpenseResponse])
    def add_expense(self, user_id: int, expenses: List[response_models.ExpenseRequest]):
        new_expense = []
        for item in expenses:
            expense = models.Expenditure(userid=user_id, **item.model_dump())
            new_expense.append(expense)
        self.db.add_all(new_expense)
        self.db.commit()
        for saved in new_expense:
            self.db.refresh(saved)
        return new_expense
    
    @expense_router.patch('/edit', response_model=response_models.ExpenseResponse)
    def edit_expense(self, user_id: int, expense_id: int, expense: response_models.EditExpenseRequest):
        expense_info = self.db.query(models.Expenditure)\
            .filter(models.Expenditure.userid==user_id)\
            .filter(models.Expenditure.id==expense_id)\
            .first()
        if not expense_info:
            raise HTTPException(status_code=404, detail=f"Record not found with id: {expense_id}")
        
        update_income = expense.model_dump(exclude_unset=True)
        for key, value in update_income.items():
            setattr(expense_info, key, value)
        
        self.db.commit()
        self.db.refresh(expense_info)
        return expense_info
    
    @expense_router.delete('/delete', response_model=response_models.ExpenseResponse)
    def delete_expense(self, user_id: int, expense_id: int, income: response_models.ExpenseRequest):
        del_expense = self.db.query(models.Expenditure)\
            .filter(models.Expenditure.id==expense_id)\
            .filter(models.Expenditure.userid==user_id)\
            .first()
        if not del_expense:
            raise HTTPException(status_code=404, detail=f"Record not found with id: {expense_id}")
        self.db.delete(del_expense)
        self.db.commit()
        return del_expense
        
        
        

