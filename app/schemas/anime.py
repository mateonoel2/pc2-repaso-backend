from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Anime(BaseModel):

    id: int
    title: str

    class Config:
        orm_mode = True
