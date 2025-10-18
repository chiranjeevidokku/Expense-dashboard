from pydantic import BaseModel

class ExpenseRequest(BaseModel):
    type: str
    amount: int
    month: str
    year: int

class EditExpenseRequest(BaseModel):
    type: str
    amount: int

class ExpenseResponse(BaseModel):
    id: int
    type: str
    userid: int
    amount: int
    month: str
    year: int

    class Config:
        from_attributes = True