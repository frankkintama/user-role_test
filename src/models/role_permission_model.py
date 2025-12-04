from api.configs.db import Base
from sqlalchemy import Column, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True)
    
    permission_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey('permissions.id', ondelete='CASCADE'),
        primary_key=True)
    
    assigned_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False)