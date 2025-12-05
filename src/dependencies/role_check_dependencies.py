from fastapi import Depends, HTTPException, status
from typing import List, Set, Callable
from api.configs.db import get_db
from src.models.user_model import User
from src.dependencies.auth_dependencies import get_current_user



def get_user_roles(user: User) -> Set[str]:
    #Lấy danh sách role của user, trả set
    if user.roles:
        return {role.role_name for role in user.roles} 
    return set()



def require_role(role_names: List[str]) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = get_user_roles(current_user)

        # Kiểm tra role của user trong set user_roles với từng role trong danh sách
        if not any(role in user_roles for role in role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User must have at least one of these roles: {role_names}"
            )
        return current_user
    
    return role_checker