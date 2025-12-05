from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional
from pwdlib import PasswordHash
from passlib.context import CryptContext


SECRET_KEY = "SECRET"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire, "type": "access"})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

