from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_db
from models.user import UserDB 
from datetime import timedelta
from sqlalchemy.orm import Session

from schemas.user import UserCreate, Token,User, LoginRequest
from services.auth import authenticate_user, create_access_token,get_user, get_password_hash

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post("/api/auth/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/api/auth/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
