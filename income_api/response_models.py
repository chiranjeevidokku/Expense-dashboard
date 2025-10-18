from pydantic import BaseModel

class IncomeRequest(BaseModel):
    type: str
    amount: int
    month: str
    year: int

class EditIncomeRequest(BaseModel):
    type: str
    amount: int

class IncomeResponse(BaseModel):
    id: int
    type: str
    userid: int
    amount: int
    month: str
    year: int

    class Config:
        from_attributes = True