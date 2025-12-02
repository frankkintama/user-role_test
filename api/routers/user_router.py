from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.schemas.user_schema import UserCreate, UserUpdate, UserOut
from src.controller.user_controller import (
    create_user, get_user, get_user_by_name, 
    list_users, update_user, delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_name(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = create_user(db, user_in)
    return user



@router.get("/get", response_model=UserOut)
def get_user_byid_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.get("/list", response_model=List[UserOut])
def list_users_endpoint(
    skip: int = Query(0, ge=0), 
    limit: int = Query(50, ge=1, le=200), 
    db: Session = Depends(get_db)
):
    users = list_users(db, skip=skip, limit=limit)
    return users



@router.put("/update", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def update_user_byid_endpoint(user_id: UUID, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = update_user(db, user, user_in)
    return user



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_byid_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return None