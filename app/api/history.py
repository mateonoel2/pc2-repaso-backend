from fastapi import APIRouter, Depends, HTTPException, Query

from typing import List

from ..models.anime import AnimeDB
from ..models.database import get_db
from ..models.history import UserHistory
from ..models.user import UserDB
from ..schemas.favorite import AnimeFavoriteRequest
from ..schemas.history import AnimeHistoryRequest, AnimeHistoryResponse
from ..services.auth import get_current_user

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/api/user/history")
def add_to_history(
    request: AnimeHistoryRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add or update an anime in the user's viewing history.

    This endpoint allows the authenticated user to add an anime to their viewing history or update its status if it already exists.

    **Request body:**

    - **anime_id**: The ID of the anime to add or update in the history.
    - **status**: The viewing status for the anime, either "viendo" or "visto".

    **Example request:**

    ```json
    {
        "anime_id": 1,
        "status": "visto"
    }
    ```

    **Example response:**

    ```json
    {
        "message": "Anime agregado/actualizado en el historial"
    }
    ```

    **Errors:**

    - **400**: Estado inválido - If the status provided is not "viendo" or "visto".
    - **404**: Anime no encontrado - If the anime with the provided ID does not exist.
    - **401**: Unauthorized - If the user is not authenticated.
    """
    if request.status not in ["viendo", "visto"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    existing_history = (
        db.query(UserHistory)
        .filter(
            UserHistory.user_id == current_user.id, UserHistory.anime_id == anime.id
        )
        .first()
    )
    if existing_history:
        existing_history.status = request.status
    else:
        new_history = UserHistory(
            user_id=current_user.id, anime_id=anime.id, status=request.status
        )
        db.add(new_history)
    db.commit()
    return {"message": "Anime agregado/actualizado en el historial"}


@router.get("/api/user/history", response_model=List[AnimeHistoryResponse])
def get_user_history(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    size: int = Query(
        10, ge=1, le=100, description="Number of items per page (between 1 and 100)"
    ),
):
    """
    Retrieve a paginated list of animes in the user's viewing history.

    This endpoint allows the authenticated user to view their anime viewing history in a paginated format.

    **Query Parameters:**

    - **page**: The page number to retrieve, starting from 1. Default is 1.
    - **size**: The number of items to return per page, between 1 and 100. Default is 10.

    **Example request:**

    ```
    GET /api/user/history?page=2&size=5
    ```

    **Example response:**

    ```json
    [
        {
            "anime_id": 1,
            "title": "Naruto",
            "status": "visto"
        },
        {
            "anime_id": 2,
            "title": "One Piece",
            "status": "viendo"
        }
    ]
    ```

    **Errors:**

    - **401**: Unauthorized - If the user is not authenticated.
    - **500**: Internal server error if there is an issue retrieving data from the database.
    """
    skip = (page - 1) * size

    history_items = (
        db.query(UserHistory)
        .filter(UserHistory.user_id == current_user.id)
        .offset(skip)
        .limit(size)
        .all()
    )

    response = [
        AnimeHistoryResponse(
            anime_id=item.anime_id, title=item.anime.title, status=item.status
        )
        for item in history_items
    ]

    return response


@router.delete("/api/user/history")
def remove_from_history(
    request: AnimeFavoriteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Remove an anime from the user's viewing history.

    This endpoint allows the authenticated user to remove a specified anime from their viewing history.

    **Request body:**

    - **anime_id**: The ID of the anime to remove from history.

    **Example request:**

    ```json
    {
        "anime_id": 1
    }
    ```

    **Example response:**

    ```json
    {
        "message": "Anime removido del historial"
    }
    ```

    **Errors:**

    - **404**: Anime no encontrado en el historial - If the anime with the provided ID is not in the user's history.
    - **401**: Unauthorized - If the user is not authenticated.
    """
    history_item = (
        db.query(UserHistory)
        .filter(
            UserHistory.user_id == current_user.id,
            UserHistory.anime_id == request.anime_id,
        )
        .first()
    )
    if not history_item:
        raise HTTPException(
            status_code=404, detail="Anime no encontrado en el historial"
        )
    db.delete(history_item)
    db.commit()
    return {"message": "Anime removido del historial"}
