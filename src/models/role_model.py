from api.configs.db import Base
from sqlalchemy import Column, String, DateTime, Boolean, text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from typing import List, TYPE_CHECKING

from uuid import uuid4

if TYPE_CHECKING:
    from src.models.user_model import User
    from src.models.permission_model import Permission

class Role(Base):
    __tablename__ = "roles"

    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    
    role_name = Column(String(255), unique=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False)
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        onupdate=text("NOW()"), 
        nullable=False)
    
    users: Mapped[List["User"]] = relationship("User", secondary="user_roles", back_populates="roles")
    permissions: Mapped[List["Permission"]] = relationship("Permission", secondary="role_permissions", back_populates="roles")