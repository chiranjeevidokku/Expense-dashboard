# response_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FinancialRecordBase(BaseModel):
    type_id: int
    subtype_id: int
    amount: int
    month: int
    year: int

class FinancialRecordCreate(FinancialRecordBase):
    pass

class FinancialRecordUpdate(BaseModel):
    amount: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

class FinancialRecordResponse(FinancialRecordBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True