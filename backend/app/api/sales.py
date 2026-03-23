"""Sales tracking API endpoints."""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.sale import SaleCreate, SaleResponse
from app.crud.sale import create_sale, get_sales, get_daily_sales_summary

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("", response_model=SaleResponse, status_code=201)
def record_sale(
    sale_in: SaleCreate,
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    """
    Record a sale. Reduces product quantity automatically.
    Returns 400 if product not found or insufficient stock.
    """
    sale = create_sale(db, sale_in, current_user.id)
    if sale is None:
        raise HTTPException(
            status_code=400,
            detail="Product not found or insufficient quantity in stock",
        )
    return sale


@router.get("", response_model=list[SaleResponse])
def list_sales(
    product_id: int | None = None,
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    """List sales with optional filters (product, date range)."""
    return get_sales(
        db,
        current_user.id,
        product_id=product_id,
        from_date=from_date,
        to_date=to_date,
        skip=skip,
        limit=limit,
    )


@router.get("/daily/{sale_date}")
def get_daily_summary(
    sale_date: date,
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    """Get daily sales summary grouped by product."""
    return get_daily_sales_summary(db, current_user.id, sale_date)
