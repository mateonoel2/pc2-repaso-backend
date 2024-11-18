from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }