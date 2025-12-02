from api.configs.db import engine, Base
from src.models.user_model import User
from src.models.role_model import Role
from src.models.user_role_model import UserRole

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("Database reset complete!")