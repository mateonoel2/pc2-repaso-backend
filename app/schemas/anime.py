from pydantic import BaseModel


class Anime(BaseModel):

    id: int
    title: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Naruto"
            }
        }