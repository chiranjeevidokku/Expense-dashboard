from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    name: str

class DeleteUser(BaseModel):
    id: int

class UserResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True