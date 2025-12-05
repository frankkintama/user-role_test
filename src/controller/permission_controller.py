from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.models.permission_model import Permission
from src.models.role_model import Role
from src.schemas.permission_schema import PermissionCreate, PermissionUpdate
from src.models.role_permission_model import RolePermission


def create_permission(db: Session, permission_in: PermissionCreate) -> Permission:
    permission = Permission(
        permission_name = permission_in.permission_name,
        description = permission_in.description
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def get_permission(db: Session, permission_id: UUID) -> Permission:
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, permission_name: str) -> Permission:
    return db.query(Permission).filter(Permission.permission_name == permission_name).first()


def list_permissions(db: Session, skip: int = 0, limit: int = 50) -> List[Permission]:
    return db.query(Permission).offset(skip).limit(limit).all()


def update_permission(db: Session, permission: Permission, permission_in: PermissionUpdate) -> Permission:
    if permission_in.permission_name is not None:
        permission.permission_name = permission_in.permission_name
    if permission_in.description is not None:
        permission.description = permission_in.description
    
    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission: Permission) -> None:
    db.delete(permission)
    db.commit()


def assign_permissions_to_role(db: Session, role: Role, permission_ids: List[UUID]) -> Role:
    for permission_id in permission_ids:
        existing = db.query(RolePermission).filter(
            RolePermission.role_id == role.id,
            RolePermission.permission_id == permission_id
        ).first()
        
        if not existing:
            role_permission = RolePermission(role_id=role.id, permission_id=permission_id)
        db.add(role_permission)
    
    db.commit()
    return role


def remove_permissions_from_role(db: Session, role: Role, permission_ids: List[UUID]) -> Role:
    db.query(RolePermission).filter(RolePermission.role_id == role.id, RolePermission.permission_id.in_(permission_ids)).delete() 
    db.commit()
    return role


def get_permissions_by_role(db: Session, role: Role) -> List[Permission]:
    return role.permissions