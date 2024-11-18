from pydantic import BaseModel


class Anime(BaseModel):

    id: int
    title: str

    class Config:
        orm_mode = True
