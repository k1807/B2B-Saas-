"""Product schemas for API validation."""
from pydantic import BaseModel
from datetime import datetime


class ProductCreate(BaseModel):
    """Schema for creating a product."""
    name: str
    sku: str
    description: str | None = None
    quantity: int = 0
    price: float = 0.0


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)."""
    name: str | None = None
    sku: str | None = None
    description: str | None = None
    quantity: int | None = None
    price: float | None = None


class ProductResponse(BaseModel):
    """Schema for product in API responses."""
    id: int
    name: str
    sku: str
    description: str | None
    quantity: int
    price: float
    created_at: datetime

    class Config:
        from_attributes = True
