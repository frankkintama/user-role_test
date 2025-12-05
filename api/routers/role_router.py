from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.schemas.role_schema import (
    RoleCreate, RoleUpdate, RoleOut, 
)
from src.schemas.user_schema import UserOut
from src.models.user_model import User
from src.models.role_model import Role
from src.controller.role_controller import (
    create_role, get_role, get_role_by_name, list_roles, 
    update_role, delete_role,
)
from src.dependencies.auth_dependencies import get_current_user
router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/create", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(
    role_in: RoleCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    existing = get_role_by_name(db, role_in.role_name)
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = create_role(db, role_in) 
    return role



@router.get("/get", response_model=RoleOut)
def get_role_endpoint(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")    
    return role


@router.get("/list", response_model=List[RoleOut])
def list_roles_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    roles = list_roles(db, skip=skip, limit=limit)
    return roles



@router.put("/update", response_model=RoleOut)
def update_role_endpoint(
    role_id: UUID, 
    role_in: RoleUpdate, 
    db: Session = Depends(get_db)
):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role_in.role_name is not None:
        existing = get_role(db, role_in.role_name)
        if existing and existing.id != role_id:
            raise HTTPException(status_code=400, detail="Role name already exists")
        
    role = update_role(db, role, role_in)
    return role



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_endpoint(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    delete_role(db, role)
    return None