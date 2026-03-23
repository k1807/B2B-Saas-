"""Product CRUD operations."""
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_products(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all products for a user with pagination."""
    return db.query(Product).filter(Product.user_id == user_id).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int, user_id: int) -> Product | None:
    """Get a single product by ID (must belong to user)."""
    return db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == user_id,
    ).first()


def get_product_by_sku(db: Session, sku: str, user_id: int) -> Product | None:
    """Get product by SKU for duplicate check."""
    return db.query(Product).filter(
        Product.sku == sku,
        Product.user_id == user_id,
    ).first()


def create_product(db: Session, product_in: ProductCreate, user_id: int) -> Product:
    """Create a new product."""
    product = Product(
        **product_in.model_dump(),
        user_id=user_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session, product: Product, product_in: ProductUpdate
) -> Product:
    """Update an existing product."""
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    """Delete a product."""
    db.delete(product)
    db.commit()
