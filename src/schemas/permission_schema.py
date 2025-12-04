from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class PermissionCreate(BaseModel):
    permission_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class PermissionUpdate(BaseModel):
    permission_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class PermissionOut(BaseModel):
    id: UUID
    permission_name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True