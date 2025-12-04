from api.configs.db import Base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from uuid import uuid4

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    
    name = Column(String(255), unique=True, nullable=False)
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
    
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")