from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session


from models.anime import AnimeDB
from models.database import get_db
from models.user import UserDB
from schemas.anime import Anime
from schemas.favorite import AnimeFavoriteRequest
from services.auth import get_current_user


router = APIRouter()


@router.get("/api/anime/list", response_model=List[Anime])
def get_anime_list(db: Session = Depends(get_db)):
    animes = db.query(AnimeDB).limit(20).all()
    return animes


@router.post("/api/user/favorites")
def add_to_favorites(
    request: AnimeFavoriteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    if anime in current_user.favorites:
        raise HTTPException(status_code=400, detail="El anime ya está en favoritos")
    current_user.favorites.append(anime)
    db.add(current_user)
    db.commit()
    return {"message": "Anime agregado a favoritos"}


@router.delete("/api/user/favorites")
def remove_from_favorites(
    request: AnimeFavoriteRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    if anime not in current_user.favorites:
        raise HTTPException(status_code=400, detail="El anime no está en favoritos")
    current_user.favorites.remove(anime)
    db.add(current_user)
    db.commit()
    return {"message": "Anime removido de favoritos"}
