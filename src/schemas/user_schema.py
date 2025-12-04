from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, date
from typing import Optional, List
from pydantic import Field

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    date_of_birth: Optional[date] = None


class UserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, min_length=3, max_length=64)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    date_of_birth: Optional[date] = None


class UserOut(BaseModel): #lấyuser
    id: UUID
    user_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class Config:
    from_attributes = True