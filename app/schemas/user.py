from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str