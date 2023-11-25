from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=25)
    email: EmailStr
    password: str = Field(min_length=1)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
