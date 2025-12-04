from api.configs.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, text, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from typing import List, TYPE_CHECKING

from uuid import uuid4

if TYPE_CHECKING:
    from src.models.role_model import Role

class User(Base):
    __tablename__ = "users"


    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    
    user_name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    phone = Column(String(10), unique=True, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False)
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        onupdate=text("NOW()"), 
        nullable=False)
    
    roles: Mapped[List["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")