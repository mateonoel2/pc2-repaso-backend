
from fastapi import APIRouter, Depends, HTTPException

from models.anime import AnimeDB
from models.database import get_db
from models.history import UserHistory
from models.user import UserDB
from schemas.favorite import AnimeFavoriteRequest
from schemas.history import AnimeHistoryRequest
from services.auth import get_current_user

from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/api/user/history")
def add_to_history(request: AnimeHistoryRequest, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    if request.status not in ["viendo", "visto"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    anime = db.query(AnimeDB).filter(AnimeDB.id == request.anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime no encontrado")
    existing_history = db.query(UserHistory).filter(
        UserHistory.user_id == current_user.id,
        UserHistory.anime_id == anime.id
    ).first()
    if existing_history:
        existing_history.status = request.status
    else:
        new_history = UserHistory(user_id=current_user.id, anime_id=anime.id, status=request.status)
        db.add(new_history)
    db.commit()
    return {"message": "Anime agregado/actualizado en el historial"}

@router.delete("/api/user/history")
def remove_from_history(request: AnimeFavoriteRequest, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    history_item = db.query(UserHistory).filter(
        UserHistory.user_id == current_user.id,
        UserHistory.anime_id == request.anime_id
    ).first()
    if not history_item:
        raise HTTPException(status_code=404, detail="Anime no encontrado en el historial")
    db.delete(history_item)
    db.commit()
    return {"message": "Anime removido del historial"}