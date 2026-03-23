"""Sale schemas for API validation."""
from pydantic import BaseModel
from datetime import date, datetime


class SaleCreate(BaseModel):
    """Schema for recording a sale."""
    product_id: int
    quantity_sold: int
    sale_date: date


class SaleResponse(BaseModel):
    """Schema for sale in API responses."""
    id: int
    product_id: int
    quantity_sold: int
    total_amount: float
    sale_date: date
    created_at: datetime

    class Config:
        from_attributes = True
