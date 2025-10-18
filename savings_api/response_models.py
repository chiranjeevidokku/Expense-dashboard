from pydantic import BaseModel

class SavingRequest(BaseModel):
    type: str
    amount: int
    month: str
    year: int

class EditSavingRequest(BaseModel):
    type: str
    amount: int

class SavingResponse(BaseModel):
    id: int
    type: str
    userid: int
    amount: int
    month: str
    year: int

    class Config:
        from_attributes = True