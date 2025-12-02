from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class RoleCreate(BaseModel):
    rolename: str = Field(..., min_length=1, max_length=255)

class RoleUpdate(BaseModel):
    rolename: Optional[str] = Field(None, min_length=1, max_length=255)

class RoleOut(BaseModel): #lấy role
    id: UUID
    rolename: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AssignRoleRequest(BaseModel):
    total_ids: List[UUID] = Field(..., min_items=1)

class RemoveRoleRequest(BaseModel):
    total_ids: List[UUID] = Field(..., min_items=1)