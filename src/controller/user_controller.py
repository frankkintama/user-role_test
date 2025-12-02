from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserUpdate
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException

def create_user(db: Session, user_in: UserCreate) -> User:

    existing = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="username or email already exists")

    user = User(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,  
        phone=user_in.phone,
        date_of_birth=user_in.date_of_birth
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()



def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    updated = False
    
    if user_in.username is not None:
        user.username = user_in.username
        updated = True
    if user_in.email is not None:
        user.email = user_in.email
        updated = True
    if user_in.password is not None:
        user.password = user_in.password
        updated = True
    if user_in.phone is not None:  
        user.phone = user_in.phone
        updated = True
    if user_in.date_of_birth is not None: 
        user.date_of_birth = user_in.date_of_birth
        updated = True
        
    if updated:
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
     