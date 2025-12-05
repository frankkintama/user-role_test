from fastapi import Depends, HTTPException, status
from typing import List, Set, Callable
from api.configs.db import get_db
from src.models.user_model import User
from src.dependencies.auth_dependencies import get_current_user



def get_user_permissions(user: User) -> Set[str]:
    permission_set: Set[str] = set()
    #Kiểm tra role của user, lặp mỗi role, kiểm tra permission của role, lặp mỗi permission
    #lặp lệnh add thêm mỗi permission tìm được vào set
    if user.roles:
        for role in user.roles:
            if role.permissions:
                for permission in role.permissions:
                    permission_set.add(permission.permission_name)
    return permission_set


def require_permission(permission_names: List[str]) -> Callable:    
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        user_permissions = get_user_permissions(current_user)

        if not any(permission in user_permissions for permission in permission_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User must have at least one of these permissions: {permission_names}"
            )
        return current_user

    return permission_checker