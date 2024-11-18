from pydantic import BaseModel


class AnimeFavoriteRequest(BaseModel):
    anime_id: int


class AnimeFavoriteResponse(BaseModel):
    anime_id: int
    title: str

    class Config:
        orm_mode = True