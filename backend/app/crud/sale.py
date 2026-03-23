"""Sale CRUD operations."""
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.sale import Sale
from app.models.product import Product
from app.schemas.sale import SaleCreate


def create_sale(db: Session, sale_in: SaleCreate, user_id: int) -> Sale | None:
    """
    Record a sale. Decreases product quantity.
    Returns None if product not found or insufficient stock.
    """
    product = db.query(Product).filter(
        Product.id == sale_in.product_id,
        Product.user_id == user_id,
    ).first()
    if not product:
        return None
    if product.quantity < sale_in.quantity_sold:
        return None
    total_amount = product.price * sale_in.quantity_sold
    sale = Sale(
        product_id=sale_in.product_id,
        user_id=user_id,
        quantity_sold=sale_in.quantity_sold,
        total_amount=total_amount,
        sale_date=sale_in.sale_date,
    )
    product.quantity -= sale_in.quantity_sold
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def get_sales(
    db: Session,
    user_id: int,
    product_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """Get sales for a user with optional filters."""
    query = db.query(Sale).filter(Sale.user_id == user_id)
    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)
    if from_date is not None:
        query = query.filter(Sale.sale_date >= from_date)
    if to_date is not None:
        query = query.filter(Sale.sale_date <= to_date)
    return query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()


def get_daily_sales_summary(
    db: Session, user_id: int, sale_date: date
) -> list[dict]:
    """Get daily sales summary grouped by product."""
    results = (
        db.query(
            Sale.product_id,
            Product.name,
            Product.sku,
            func.sum(Sale.quantity_sold).label("total_qty"),
            func.sum(Sale.total_amount).label("total_revenue"),
        )
        .join(Product, Sale.product_id == Product.id)
        .filter(Sale.user_id == user_id, Sale.sale_date == sale_date)
        .group_by(Sale.product_id, Product.name, Product.sku)
        .all()
    )
    return [
        {
            "product_id": r.product_id,
            "product_name": r.name,
            "sku": r.sku,
            "quantity_sold": r.total_qty,
            "revenue": float(r.total_revenue),
        }
        for r in results
    ]
