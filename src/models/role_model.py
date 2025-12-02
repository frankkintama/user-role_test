from api.configs.db import Base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from uuid import uuid4

class Role(Base):
    __tablename__ = "roles"

    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4)
    
    rolename = Column(String(255), unique=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False)
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        onupdate=text("NOW()"), 
        nullable=False)
    
    users = relationship("User", secondary="user_roles", back_populates="roles")