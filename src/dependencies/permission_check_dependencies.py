
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


