from api.configs.db import Base, engine
from sqlalchemy import text

from src.models.user_role_model import UserRole
from src.models.role_permission_model import RolePermission


from src.models.user_model import User
from src.models.role_model import Role
from src.models.permission_model import Permission
from src.models.blacklist_model import TokenBlacklist

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset complete!")