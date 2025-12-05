from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.models.user_model import User
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.schemas.permission_schema import PermissionCreate, PermissionUpdate, PermissionOut
from src.controller.permission_controller import (
    create_permission, get_permission, get_permission_by_name,
    list_permissions, update_permission, delete_permission,
    assign_permissions_to_role, remove_permissions_from_role,
    get_permissions_by_role
)
from src.controller.role_controller import get_role
from src.dependencies.auth_dependencies import get_current_user
from src.dependencies.role_check_dependencies import get_role_dependency, require_role
from src.dependencies.permission_check_dependencies import get_permission_dependency, require_permission


router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/create", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission_endpoint(
    permission_in: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = get_permission_by_name(db, permission_in.permission_name)
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    permission = create_permission(db, permission_in)
    return permission


@router.get("/get", response_model=PermissionOut)
def get_permission_endpoint(
    permission: Permission = Depends(get_permission_dependency)
):
    return permission


@router.get("/list", response_model=List[PermissionOut])
def list_permissions_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    permissions = list_permissions(db, skip=skip, limit=limit)
    return permissions



@router.put("/update", response_model=PermissionOut)
def update_permission_endpoint(
    permission_in: PermissionUpdate,
    permission: Permission = Depends(get_permission_dependency),
    db: Session = Depends(get_db)
):
    if permission_in.permission_name is not None:
        existing = get_permission_by_name(db, permission_in.permission_name)
        if existing and existing.id != permission.id:
            raise HTTPException(status_code=400, detail="Permission name already exists")
    
    permission = update_permission(db, permission, permission_in)
    return permission


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission_endpoint(
    permission: Permission = Depends(get_permission_dependency), 
    db: Session = Depends(get_db)
):
    delete_permission(db, permission)
    return None



@router.post("/assign_role_with_permissions/")
def assign_role_with_permission_endpoint(
    permission_ids: List[UUID] = Body(..., min_length=1),
    role: Role = Depends(get_role_dependency),
    db: Session = Depends(get_db)
):
    
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    if len(permissions) != len(permission_ids):
        found_ids = {Permission.id in permissions}
        missing_ids = set(permission_ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Permissions not found: {list(missing_ids)}"
        )
    
    role = assign_permissions_to_role(db, role, permission_ids)
    return {
        "message": f"Successfully assigned permissions for role {role.id}",
    }



@router.delete("/remove_role_from_permissions/")
def remove_permissions_from_role_endpoint(
    permission_ids: List[UUID] = Body(..., min_length=1),
    role: Role = Depends(get_role_dependency),
    db: Session = Depends(get_db),
    current_user_role: User = Depends(require_role(["Admin"])),
    current_user_permission: User = Depends(require_permission([""]))
):
       
    role = remove_permissions_from_role(db, role, permission_ids)
    return {
        "message": f"Successfully removed permissions from role {role.id}",
    }


@router.get("/get_permissons_with_role", response_model=List[PermissionOut])
def get_permissions_by_role_endpoint(
    role: Role = Depends(get_role_dependency), 
    db: Session = Depends(get_db)
):
    permissions = get_permissions_by_role(db, role)
    return permissions