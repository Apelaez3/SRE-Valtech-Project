from pydantic import BaseModel

class  UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

    class Config:
        orm_mode = True