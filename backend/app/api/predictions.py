"""AI-powered demand prediction endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.crud.prediction import (
    get_daily_demand,
    get_top_product_by_sales,
    forecast_demand,
    get_trend,
)

router = APIRouter(prefix="/predict-demand", tags=["predictions"])


@router.get("")
def predict_demand(
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,
):
    """
    Predict demand for the next 7 days using sales history.
    Uses simple linear regression on recent daily sales.
    """
    points = get_daily_demand(db, current_user.id, days=30)
    predictions = forecast_demand(points, horizon=7)
    trend = get_trend(points) if points else "stable"
    top_product = get_top_product_by_sales(db, current_user.id)

    if trend == "increasing" and top_product:
        message = f"Expected increase in demand for top product: {top_product['name']} ({top_product['sku']})"
    elif trend == "decreasing" and top_product:
        message = f"Demand may decrease for {top_product['name']}. Consider promotions."
    elif trend == "stable" and top_product:
        message = f"Stable demand expected. Top seller: {top_product['name']}"
    else:
        message = "Record more sales to improve predictions."

    return {
        "predictions": predictions,
        "trend": trend,
        "message": message,
        "top_product": top_product,
        "historical_days_used": len(points),
    }
