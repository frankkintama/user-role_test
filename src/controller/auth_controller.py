from sqlalchemy.orm import Session
from src.models.user_model import User
from src.models.blacklist_model import TokenBlacklist
from src.schemas.auth_schema import UserRegister
from api.configs.auth import get_password_hash, verify_password
from typing import Optional
from datetime import datetime, timedelta, timezone

def create_user_account(db: Session, user_data: UserRegister) -> User:
    hashed_password = get_password_hash(user_data.password)
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def blacklist_token(db: Session, token: str, expires_at: datetime) -> None:
    blacklisted = TokenBlacklist(token=token, expires_at=expires_at)
    db.add(blacklisted)
    db.commit()


def is_token_blacklisted(db: Session, token: str) -> bool:
    result = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    return result is not None


#def cleanup_expired_tokens(db: Session) -> None:
#   db.query(TokenBlacklist).filter(TokenBlacklist.expires_at < datetime.now(timezone.utc)).delete(synchronize_session=False)
#   db.commit()