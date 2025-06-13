from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session


from ..models.anime import AnimeDB
from ..models.database import get_db
from ..models.user import UserDB
from ..schemas.anime import Anime
from ..schemas.favorite import AnimeFavoriteRequest, AnimeFavoriteResponse
from ..services.auth import get_current_user


router = APIRouter()


@router.post("/api/user/favorites")
def add_to_favorites(
    request: AnimeFavoriteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add an anime to the user's list of favorites.

    This endpoint allows the authenticated user to add a specified anime to their favorites list.

    **Request body:**

    - **anime_id**: The ID of the anime to add to favorites.

    **Example request:**

    ```json
    {
        "anime_id": 1
    }
    ```

    **Example response:**

    ```json
    {
        "message": "Anime agregado a favoritos"
    }
    ```

    **Errors:**

    - **404**: Anime no encontrado - If the anime with the provided ID does not exist.
    - **400**: El anime ya está en favoritos - If the anime is already in the user's favorites.
    - **401**: Unauthorized - If the user is not authenticated.
    """
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    if anime in current_user.favorites:
        raise HTTPException(status_code=400, detail="El anime ya está en favoritos")
    current_user.favorites.append(anime)
    db.add(current_user)
    db.commit()
    return {"message": "Anime agregado a favoritos"}


@router.get("/api/user/favorites", response_model=List[AnimeFavoriteResponse])
def get_user_favorites(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    size: int = Query(
        10, ge=1, le=100, description="Number of items per page (between 1 and 100)"
    ),
):
    """
    Retrieve a paginated list of animes in the user's favorites.

    This endpoint allows the authenticated user to view their favorite animes in a paginated format.

    **Query Parameters:**

    - **page**: The page number to retrieve, starting from 1. Default is 1.
    - **size**: The number of items to return per page, between 1 and 100. Default is 10.

    **Example request:**

    ```
    GET /api/user/favorites?page=2&size=5
    ```

    **Example response:**

    ```json
    [
        {
            "anime_id": 1,
            "title": "Naruto"
        },
        {
            "anime_id": 2,
            "title": "One Piece"
        }
    ]
    ```

    **Errors:**

    - **401**: Unauthorized - If the user is not authenticated.
    - **500**: Internal server error if there is an issue retrieving data from the database.
    """
    skip = (page - 1) * size

    favorites = (
        db.query(AnimeDB)
        .join(UserDB.favorites)
        .filter(UserDB.id == current_user.id)
        .offset(skip)
        .limit(size)
        .all()
    )

    response = [
        AnimeFavoriteResponse(anime_id=anime.id, title=anime.title)
        for anime in favorites
    ]

    return response


@router.delete("/api/user/favorites")
def remove_from_favorites(
    request: AnimeFavoriteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remove an anime from the user's list of favorites.

    This endpoint allows the authenticated user to remove a specified anime from their favorites list.

    **Request body:**

    - **anime_id**: The ID of the anime to remove from favorites.

    **Example request:**

    ```json
    {
        "anime_id": 1
    }
    ```

    **Example response:**

    ```json
    {
        "message": "Anime removido de favoritos"
    }
    ```

    **Errors:**

    - **404**: Anime no encontrado - If the anime with the provided ID does not exist.
    - **400**: El anime no está en favoritos - If the anime is not in the user's favorites.
    - **401**: Unauthorized - If the user is not authenticated.
    """
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    if anime not in current_user.favorites:
        raise HTTPException(status_code=400, detail="El anime no está en favoritos")
    current_user.favorites.remove(anime)
    db.add(current_user)
    db.commit()
    return {"message": "Anime removido de favoritos"}
