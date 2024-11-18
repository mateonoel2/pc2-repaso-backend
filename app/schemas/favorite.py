from pydantic import BaseModel


class AnimeFavoriteRequest(BaseModel):
    anime_id: int
