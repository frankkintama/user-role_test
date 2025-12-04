from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class PermissionCreate(BaseModel):
    permissionname: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class PermissionUpdate(BaseModel):
    permissionname: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)

class PermissionOut(BaseModel):
    id: UUID
    permissionname: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True