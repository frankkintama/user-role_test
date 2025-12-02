from api.configs.db import Base
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from uuid import uuid4

class TokenBlacklist(Base):
    __tablename__ = "blacklist_token"

    id = Column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4
    )
    
    token = Column(String, unique=True, nullable=False)
    
    blacklisted_at = Column(
        DateTime(timezone=True), 
        server_default=text("NOW()"), 
        nullable=False
    )
    
    expires_at = Column(DateTime(timezone=True), nullable=False)