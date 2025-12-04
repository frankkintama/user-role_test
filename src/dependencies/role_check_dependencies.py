from fastapi import Depends, HTTPException, status
from typing import List, Set
from api.configs.db import get_db
from src.models.user_model import User
from src.dependencies.auth_dependencies import get_current_user

def get_user_roles(user: User) -> Set[str]:
    #kiểm tra role của user, lặp mỗi role, lặp lệnh add thêm mỗi role tìm được vào set
    if user.roles:
        return {role.rolename for role in user.roles} #chạy thành set, loại bỏ trùng lặp
    return set()


def require_role(role_names: List[str], current_user: User = Depends(get_current_user)):
        user_roles = get_user_roles(current_user)
        
        if not any(role in user_roles for role in role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User must have at least one of these roles: {role_names}"
            )
        
        return current_user