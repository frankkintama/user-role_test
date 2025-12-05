from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.models.user_model import User
from src.models.role_model import Role
from src.schemas.user_schema import UserCreate, UserUpdate, UserOut
from src.schemas.role_schema import RoleOut
from src.controller.user_controller import (
    create_user, get_user, get_user_by_name, 
    list_users, update_user, delete_user
)
from src.controller.role_controller import (get_role, assign_users_with_role, remove_role_from_users, get_users_by_role)
from src.dependencies.auth_dependencies import get_current_user
from src.dependencies.user_dependencies import get_user_dependency
from src.dependencies.role_check_dependencies import get_role_dependency, require_role
from src.dependencies.permission_check_dependencies import require_permission
from src.models.user_model import User


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_in: UserCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    existing = get_user_by_name(db, user_in.user_name)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = create_user(db, user_in)
    return user



@router.get("/get", response_model=UserOut)
def get_user_byid_endpoint(
    user: User = Depends(get_user_dependency),
    db: Session = Depends(get_db)
):
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
def update_user_byid_endpoint(
    user_in: UserUpdate, 
    user: User = Depends(get_user_dependency),
    db: Session = Depends(get_db)
):
    user = update_user(db, user, user_in)
    return user



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_byid_endpoint(
    user: User = Depends(get_user_dependency),
    db: Session = Depends(get_db)
):
    delete_user(db, user)
    return None


@router.post("/assign_role_to_users")
def assign_role_to_user_endpoint(
    role: Role = Depends(get_role_dependency), 
    user_ids: List[UUID] = Body(..., min_length=1),
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    if len(users) != len(user_ids):
        found_ids = {User.id in users}
        missing_ids = set(user_ids) - found_ids
        raise HTTPException(status_code=404, detail=f"Users not found: {list(missing_ids)}")
    
    role = assign_users_with_role(db, role, user_ids)
    return {
        "message": f"Successfully assigned role to users {user_ids}",
    }



@router.delete("/remove_role_from_users")
def remove_role_from_users_endpoint(
    role: Role = Depends(get_role_dependency), 
    user_ids: List[UUID] = Body(..., min_length=1),
    db: Session = Depends(get_db),
    current_user_role: User = Depends(require_role(["Admin"])),
    current_user_permission: User = Depends(require_permission([""]))
):
    role = remove_role_from_users(db, role, user_ids)
    return {
        "message": f"Successfully removed role from from users {user_ids}"
    }


@router.get("/get_users_with_role", response_model=List[UserOut])
def get_role_by_users_endpoint(
    role: Role = Depends(get_role_dependency), 
    db: Session = Depends(get_db)
):
    users = get_users_by_role(db, role)
    return users