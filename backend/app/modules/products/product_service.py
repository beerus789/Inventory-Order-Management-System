"""Product service containing business logic."""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.core import (
    InvalidProductPriceException,
    InvalidProductQuantityException,
    ProductNotFoundException,
    ProductSKUAlreadyExistsException,
)

from .product_model import Product
from .product_repository import ProductRepository


class ProductService:
    """Service layer for product operations."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.repository = ProductRepository(db)

    def create_product(
        self, name: str, sku: str, price: Decimal, quantity: int
    ) -> Product:
        """Create a new product with validation."""
        # Validate price
        if price < 0:
            raise InvalidProductPriceException(price)

        # Validate quantity
        if quantity < 0:
            raise InvalidProductQuantityException(quantity)

        # Check if SKU already exists
        existing = self.repository.get_by_sku(sku)
        if existing:
            raise ProductSKUAlreadyExistsException(sku)

        return self.repository.create(name, sku, price, quantity)

    def get_product(self, product_id: int) -> Product:
        """Get product by ID."""
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product

    def get_all_products(self) -> list[Product]:
        """Get all products."""
        return self.repository.get_all()

    def update_product(
        self, product_id: int, name: str = None, price: Decimal = None, quantity: int = None
    ) -> Product:
        """Update product with validation."""
        product = self.get_product(product_id)

        # Validate price if provided
        if price is not None and price < 0:
            raise InvalidProductPriceException(price)

        # Validate quantity if provided
        if quantity is not None and quantity < 0:
            raise InvalidProductQuantityException(quantity)

        return self.repository.update(product, name=name, price=price, quantity=quantity)

    def delete_product(self, product_id: int) -> None:
        """Delete a product."""
        product = self.get_product(product_id)
        self.repository.delete(product)

    def get_low_stock_products(self, threshold: int = 5) -> list[Product]:
        """Get products with stock below threshold."""
        return [p for p in self.get_all_products() if p.quantity <= threshold]
