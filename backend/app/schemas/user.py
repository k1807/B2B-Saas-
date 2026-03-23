"""User schemas for API validation."""
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user in API responses."""
    id: int
    email: str
    full_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True
