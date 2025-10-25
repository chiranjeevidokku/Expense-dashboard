from pydantic import BaseModel
from typing import Optional

class TransactionBaseModel(BaseModel):
    transtype_id: int
    subtype_id: int
    amount: int
    month: int
    year: int

class TransactionResponsetModel(TransactionBaseModel):
    id: int
    user_id: int

class TransactionCreateRecord(TransactionBaseModel):
    pass

class TransactionUpdateRecord(BaseModel):
    amount: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

