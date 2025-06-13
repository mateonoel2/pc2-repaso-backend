from fastapi import APIRouter, Depends, HTTPException, status
from ..models.database import get_db
from ..models.user import UserDB
from datetime import timedelta
from sqlalchemy.orm import Session

from ..schemas.user import UserCreate, Token, User, LoginRequest
from ..services.auth import (
    authenticate_user,
    create_access_token,
    get_user,
    get_password_hash,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/api/auth/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint allows users to register by providing an email and a password.

    - **email**: The user's unique email address. Required for authentication.
    - **password**: The password for the user account.

    **Example request:**

    ```json
    {
        "email": "user@example.com",
        "password": "strongpassword123"
    }
    ```

    **Example response:**

    ```json
    {
        "id": 1,
        "email": "user@example.com"
    }
    ```

    **Errors:**

    - **400**: The email is already registered.
    - **422**: Invalid input data (e.g., invalid email format).

    """
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
    """
    Log in a user.

    This endpoint authenticates a user by verifying their email and password, and returns an access token.

    - **email**: The user's email address.
    - **password**: The password for the user account.

    **Example request:**

    ```json
    {
        "email": "user@example.com",
        "password": "strongpassword123"
    }
    ```

    **Example response:**

    ```json
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "bearer"
    }
    ```

    **Errors:**

    - **401**: Email or password is incorrect.
    - **422**: Invalid input data (e.g., missing email or password).

    The access token is a JWT token that must be used in the `Authorization` header
    for authenticated requests, like this:

    ```
    Authorization: Bearer <access_token>
    ```
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
