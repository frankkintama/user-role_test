from api.configs.db import Base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from typing import List, TYPE_CHECKING

from uuid import uuid4

if TYPE_CHECKING:
    from src.models.role_model import Role

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    
    permissionname = Column(String(255), unique=True, nullable=False)
    description = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False)
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        onupdate=text("NOW()"), 
        nullable=False)
    
    roles: Mapped[List["Role"]] = relationship("Role", secondary="role_permissions", back_populates="permissions")