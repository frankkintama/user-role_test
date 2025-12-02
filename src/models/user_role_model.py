from api.configs.db import Base
from sqlalchemy import Column, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True)
    
    role_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True)
    
    assigned_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False)