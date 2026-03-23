"""Sale model for daily sales tracking."""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False)  # Daily tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    product = relationship("Product", back_populates="sales")
    user = relationship("User", back_populates="sales")
