from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.schemas.role_schema import (
    RoleCreate, RoleUpdate, RoleOut, 
    AssignRoleRequest, RemoveRoleRequest
)
from src.schemas.user_schema import UserOut
from src.models.user_model import User
from src.controller.role_controller import (
    create_role, get_role, get_role_by_name, list_roles, 
    update_role, delete_role, assign_role, 
    remove_role_from_users, get_users_by_role
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/create", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(role_in: RoleCreate, db: Session = Depends(get_db)):
    existing = get_role_by_name(db, role_in.rolename)
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
    
    if role_in.rolename is not None:
        existing = get_role(db, role_in.rolename)
        if existing and existing.id != role_id:
            raise HTTPException(status_code=400, detail="Role name already exists")
        
    role = update_role(db, role, role_in)
    return role





@router.post("/assign_role", response_model=RoleOut)
def assign_role_endpoint(
    role_id: UUID,
    request: AssignRoleRequest,
    db: Session = Depends(get_db)
):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    users = db.query(User).filter(User.id.in_(request.total_ids)).all()
    if len(users) != len(request.total_ids):
        found_ids = {user.id for user in users}
        missing_ids = set(request.total_ids) - found_ids
        raise HTTPException(status_code=404, detail=f"Users not found: {list(missing_ids)}")
    
    role = assign_role(db, role, role_id, request.total_ids)
    return role



@router.get("/list/get_users_with_role", response_model=List[UserOut])
def get_role_by_users_endpoint(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    users = get_users_by_role(db, role)
    return users




@router.delete("/remove_role_from_users", response_model=RoleOut)
def remove_role_from_users_endpoint(
    role_id: UUID,
    request: RemoveRoleRequest,
    db: Session = Depends(get_db)
):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role = remove_role_from_users(db, role, role_id, request.total_ids)
    return role



@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_endpoint(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    delete_role(db, role)
    return None