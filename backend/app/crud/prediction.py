"""Helpers for demand forecasting - uses simple moving average + linear trend."""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.sale import Sale


def get_daily_demand(db: Session, user_id: int, days: int = 30) -> list[tuple[date, float]]:
    """Get total quantity sold per day for the last N days."""
    cutoff = date.today() - timedelta(days=days)
    rows = (
        db.query(Sale.sale_date, func.sum(Sale.quantity_sold).label("qty"))
        .filter(Sale.user_id == user_id, Sale.sale_date >= cutoff)
        .group_by(Sale.sale_date)
        .order_by(Sale.sale_date)
        .all()
    )
    return [(r.sale_date, float(r.qty or 0)) for r in rows]


def get_top_product_by_sales(db: Session, user_id: int) -> dict | None:
    """Get the top-selling product (by quantity) from recent sales."""
    from app.models.product import Product
    cutoff = date.today() - timedelta(days=30)
    row = (
        db.query(Product.name, Product.sku, func.sum(Sale.quantity_sold).label("total"))
        .join(Sale, Sale.product_id == Product.id)
        .filter(Sale.user_id == user_id, Sale.sale_date >= cutoff)
        .group_by(Product.id, Product.name, Product.sku)
        .order_by(func.sum(Sale.quantity_sold).desc())
        .first()
    )
    if row and row.total:
        return {"name": row.name, "sku": row.sku}
    return None


def forecast_demand(points: list[tuple[date, float]], horizon: int = 7) -> list[dict]:
    """
    Simple linear regression forecast for next N days.
    Uses last 14 days of data (or less if not enough).
    """
    if not points or horizon <= 0:
        return []

    points = points[-14:]  # Use last 14 days
    n = len(points)
    if n < 2:
        avg = points[0][1] if points else 0
        start = points[0][0] + timedelta(days=1) if points else date.today()
        return [{"date": str(start + timedelta(days=i)), "predicted_demand": round(avg, 1)} for i in range(horizon)]

    # Simple linear regression: y = slope * x + intercept
    x = list(range(n))
    y = [p[1] for p in points]
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean

    last_date = points[-1][0]
    predictions = []
    for i in range(1, horizon + 1):
        pred_date = last_date + timedelta(days=i)
        pred_val = max(0, slope * (n - 1 + i) + intercept)
        predictions.append({"date": str(pred_date), "predicted_demand": round(pred_val, 1)})

    return predictions


def get_trend(points: list[tuple[date, float]]) -> str:
    """Return 'increasing', 'decreasing', or 'stable' based on recent data."""
    if len(points) < 2:
        return "stable"
    first_half = sum(p[1] for p in points[: len(points) // 2]) / max(1, len(points) // 2)
    second_half = sum(p[1] for p in points[len(points) // 2 :]) / max(1, len(points) - len(points) // 2)
    diff = second_half - first_half
    if diff > 0.5:
        return "increasing"
    if diff < -0.5:
        return "decreasing"
    return "stable"
