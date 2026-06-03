"""Product database model."""

from decimal import Decimal

from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, TimestampMixin


class Product(Base, TimestampMixin):
    """Product model representing products in inventory."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, sku={self.sku}, price={self.price}, quantity={self.quantity})>"
