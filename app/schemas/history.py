from pydantic import BaseModel


class AnimeHistoryRequest(BaseModel):
    anime_id: int
    status: str
