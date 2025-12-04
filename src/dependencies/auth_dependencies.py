from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.configs.db import get_db
from api.configs.auth import verify_token
from src.models.user_model import User
from src.controller.auth_controller import is_token_blacklisted
from uuid import UUID


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
bearer_scheme = HTTPBearer()


def get_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return credentials.credentials


def get_payload(token: str = Depends(get_token)):
    return verify_token(token)


def get_current_user(
    token: str = Depends(get_token),
    payload: dict = Depends(get_payload),
    db: Session = Depends(get_db)
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    if is_token_blacklisted(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    user_id: str = payload.get("user_id")
    token_type: str = payload.get("type")
    
    if username is None or user_id is None:
        raise credentials_exception
    
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )   
    return user
