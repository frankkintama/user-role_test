from sqlalchemy.orm import Session
from src.models.user_model import User
from src.models.role_model import Role
from src.models.user_role_model import UserRole
from src.schemas.role_schema import RoleCreate, RoleUpdate, AssignRoleRequest, RemoveRoleRequest
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException

def create_role(db: Session, role_in: RoleCreate) -> Role:
    role = Role(
        rolename=role_in.rolename,
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_role(db: Session, role_id: UUID) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, rolename: str) -> Optional[Role]:
    return db.query(Role).filter(Role.rolename == rolename).first()


def list_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    return db.query(Role).offset(skip).limit(limit).all()


def update_role(db: Session, role: Role, role_in: RoleUpdate) -> Role:
    updated = False
    
    if role_in.rolename is not None:
        role.rolename = role_in.rolename
        updated = True
        
    if updated:
        db.add(role)
        db.commit()
        db.refresh(role)
    return role



def assign_role(db: Session, role: Role, role_id: UUID, total_ids: List[UUID]) -> Role:
    # Assign roles (avoid duplicates)
    # client gửi request gán role cho 1 hoặc nhiều user, hàm kiểm tra id của user
    # Kiểm tra db bảng user_roles trong UserRole lấy giá trị id của user và role đầu tiên nếu tồn tại
    # Nếu không tồn tại thì tạo mới UserRole và thêm vào db
    for user_id in total_ids:
        existing = db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        ).first()
        
        if not existing:
            user_role = UserRole(user_id=user_id, role_id=role_id)
        # bỏ db.add() ở đây để db.add() hoạt động trong vòng lặp, ghi id_role cho mỗi id_user không tìm thấy trong bảng trung gian user_roles
        db.add(user_role)
    
    db.commit()
    db.refresh(role)
    return role



def remove_role_from_users(db: Session, role: Role, role_id: UUID, total_ids: List[UUID]) -> Role:
    db.query(UserRole).filter(UserRole.role_id == role_id, UserRole.user_id.in_(total_ids)).delete(synchronize_session=False) 
    db.commit()
    db.refresh(role)
    return role
    

def get_users_by_role(db: Session, role:Role) -> List[User]:
    return role.users


def delete_role(db: Session, role: Role) -> None:
    db.delete(role)
    db.commit()