from pydantic import BaseModel


class AnimeHistoryRequest(BaseModel):
    anime_id: int
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "anime_id": 1,
                "status": "visto"
            }
        }

class AnimeHistoryResponse(BaseModel):
    anime_id: int
    title: str
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "anime_id": 1,
                "title": "Naruto",
                "status": "visto"
            }
        }
