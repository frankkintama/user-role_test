from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.configs.db import get_db
from api.configs.auth import create_access_token
from src.controller.auth_controller import blacklist_token
from datetime import datetime, timezone
from src.schemas.auth_schema import UserRegister, Token
from src.schemas.user_schema import UserOut
from src.controller.auth_controller import (
    create_user_account,
    authenticate_user,
)

from src.controller.user_controller import get_user_by_name
from src.dependencies.auth_dependencies import get_current_user, get_token, get_payload
from src.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_name(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = create_user_account(db, user_data)
    return user



@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username, "user_id": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    current_user: User = Depends(get_current_user),
    token: str = Depends(get_token),
    payload: dict = Depends(get_payload),
    db: Session = Depends(get_db),
):    

    if not payload or not payload.get("exp"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token payload"
        )

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    
    blacklist_token(db, token, expires_at)
    
    return {
        "message": f"User {current_user} successfully logged out. Token has been revoked."
    }


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user