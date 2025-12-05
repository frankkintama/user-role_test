from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from api.configs.db import get_db
from src.controller.user_controller import get_user_by_id
from uuid import UUID


def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user