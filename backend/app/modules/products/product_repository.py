"""Product repository for database operations."""

from typing import Optional

from sqlalchemy.orm import Session

from .product_model import Product


class ProductRepository:
    """Repository for product database operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, name: str, sku: str, price, quantity: int) -> Product:
        """Create a new product."""
        product = Product(name=name, sku=sku, price=price, quantity=quantity)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        return self.db.query(Product).filter(Product.sku == sku.upper()).first()

    def get_all(self) -> list[Product]:
        """Get all products."""
        return self.db.query(Product).all()

    def update(self, product: Product, **kwargs) -> Product:
        """Update product fields."""
        for key, value in kwargs.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        """Delete a product."""
        self.db.delete(product)
        self.db.commit()

    def reduce_stock(self, product: Product, quantity: int) -> Product:
        """Reduce product stock."""
        product.quantity -= quantity
        self.db.add(product)
        self.db.flush()
        return product

    def increase_stock(self, product: Product, quantity: int) -> Product:
        """Increase product stock."""
        product.quantity += quantity
        self.db.add(product)
        self.db.flush()
        return product
