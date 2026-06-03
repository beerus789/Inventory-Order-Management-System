"""Order repository for database operations."""

from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session, joinedload, selectinload

from .order_item_model import OrderItem
from .order_model import Order, OrderStatus


class OrderRepository:
    """Repository for order database operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, customer_id: int, total_amount: Decimal, status: OrderStatus = OrderStatus.PENDING) -> Order:
        """Create a new order."""
        order = Order(customer_id=customer_id, total_amount=total_amount, status=status)
        self.db.add(order)
        self.db.flush()  # Flush to get the order ID without committing yet
        return order

    def create_order_item(
        self, order_id: int, product_id: int, quantity: int, unit_price: Decimal
    ) -> OrderItem:
        """Create an order item."""
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.db.add(item)
        return item

    def commit(self) -> None:
        """Commit transaction."""
        self.db.commit()

    def rollback(self) -> None:
        """Rollback transaction."""
        self.db.rollback()

    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                selectinload(Order.items).joinedload(OrderItem.product),
            )
            .filter(Order.id == order_id)
            .first()
        )

    def get_all(self) -> list[Order]:
        """Get all orders."""
        return (
            self.db.query(Order)
            .options(
                joinedload(Order.customer),
                selectinload(Order.items).joinedload(OrderItem.product),
            )
            .order_by(Order.created_at.desc())
            .all()
        )

    def delete(self, order: Order) -> None:
        """Delete an order."""
        self.db.delete(order)
        self.db.commit()

    def update_status(self, order: Order, status: OrderStatus) -> Order:
        """Update order status."""
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
