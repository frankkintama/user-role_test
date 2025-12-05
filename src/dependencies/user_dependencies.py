from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.user_model import User
from src.models.role_model import Role
from api.configs.db import get_db
from uuid import UUID
from src.controller.user_controller import get_user



def get_user_dependency(
    user_id: UUID, 
    db: Session = Depends(get_db)
) -> User:
    
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return user