from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from sqlalchemy.orm import Session
from src.models.user_model import User
from typing import List
from uuid import UUID

from api.configs.db import get_db
from src.schemas.permission_schema import PermissionCreate, PermissionUpdate, PermissionOut
from src.schemas.role_schema import RoleOut
from src.models.permission_model import Permission
from src.controller.permission_controller import (
    create_permission, get_permission, get_permission_by_name,
    list_permissions, update_permission, delete_permission,
    assign_permissions_to_role, remove_permissions_from_role,
    get_permissions_by_role
)
from src.controller.role_controller import get_role
from src.dependencies.auth_dependencies import get_current_user
from src.dependencies.permission_check_dependencies import require_permission
from src.dependencies.role_check_dependencies import require_role

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/create", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission_endpoint(
    permission_in: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = get_permission_by_name(db, permission_in.permissionname)
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    permission = create_permission(db, permission_in)
    return permission


@router.get("/get", response_model=PermissionOut)
def get_permission_endpoint(permission_id: UUID, db: Session = Depends(get_db)):
    permission = get_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
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
    permission_id: UUID,
    permission_in: PermissionUpdate,
    db: Session = Depends(get_db)
):
    permission = get_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    if permission_in.permissionname is not None:
        existing = get_permission_by_name(db, permission_in.permissionname)
        if existing and existing.id != permission_id:
            raise HTTPException(status_code=400, detail="Permission name already exists")
    
    permission = update_permission(db, permission, permission_in)
    return permission


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission_endpoint(permission_id: UUID, db: Session = Depends(get_db)):
    permission = get_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    delete_permission(db, permission)
    return None


@router.post("/assign_role_with_permissions/", response_model=RoleOut)
def assign_role_with_permission_endpoint(
    role_id: UUID,
    permission_ids: List[UUID] = Body(..., min_length=1),
    db: Session = Depends(get_db)
):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    if len(permissions) != len(permission_ids):
        found_ids = {Permission.id in permissions}
        missing_ids = set(permission_ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Permissions not found: {list(missing_ids)}"
        )
    
    role = assign_permissions_to_role(db, role, role_id, permission_ids)
    return role


@router.delete("/remove_role_from_permissions/", response_model=RoleOut)
def remove_permissions_from_role_endpoint(
    role_id: UUID,
    permission_ids: List[UUID] = Body(..., min_length=1),
    db: Session = Depends(get_db),
    current_role: User = Depends(require_role("Admin")),
    current_permission: User = Depends(require_permission("remove_role_from_permissions"))
):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    if len(permissions) != len(permission_ids):
        found_ids = {p.id for p in permissions}
        missing_ids = set(permission_ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Permissions not found: {list(missing_ids)}"
        )
    
    role = remove_permissions_from_role(db, role, role_id, permission_ids)
    return role


@router.get("/get_permissons_with_role", response_model=List[PermissionOut])
def get_permissions_by_role_endpoint(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    permissions = get_permissions_by_role(db, role)
    return permissions