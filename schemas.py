from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     name: str
    
#     class Config:
#         from_attributes = True


# class CreateUser(BaseModel):
#     name: str

# class DeleteUser(BaseModel):
#     id: int

# class UserResponse(BaseModel):
#     id: int
#     name: str
    
#     class Config:
#         from_attributes = True

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
