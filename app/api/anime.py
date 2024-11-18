from typing import List
from fastapi import APIRouter, Depends

from models import anime, database
from schemas.anime import Anime

from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/anime/list", response_model=List[Anime])
def get_anime_list(db: Session = Depends(database.get_db)):
    animes = db.query(anime.AnimeDB).limit(20).all()
    return animes
