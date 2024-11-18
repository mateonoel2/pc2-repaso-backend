from typing import List
from fastapi import APIRouter, Depends, Query

from models import anime, database
from schemas.anime import Anime

from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/api/anime/list", response_model=List[Anime])
def get_anime_list(
    db: Session = Depends(database.get_db),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    size: int = Query(
        10, ge=1, le=100, description="Number of items per page (between 1 and 100)"
    ),
):
    """
    Retrieve a paginated list of animes available on the platform.

    This endpoint allows users to view a paginated list of anime titles. Use the `page` and `size` query parameters to control pagination.

    - **page**: The page number to retrieve, starting from 1. Default is 1.
    - **size**: The number of items to return per page, between 1 and 100. Default is 10.

    **Example request:**

    ```
    GET /api/anime/list?page=2&size=5
    ```

    **Example response:**

    ```json
    [
        {
            "id": 1,
            "title": "Naruto"
        },
        {
            "id": 2,
            "title": "One Piece"
        },
        {
            "id": 3,
            "title": "Attack on Titan"
        },
        ...
    ]
    ```

    **Errors:**

    - **422**: Validation error if `page` or `size` are out of the allowed range.

    - **500**: Internal server error if there is a problem retrieving data from the database.

    """

    skip = (page - 1) * size

    animes = db.query(anime.AnimeDB).offset(skip).limit(size).all()
    return animes
