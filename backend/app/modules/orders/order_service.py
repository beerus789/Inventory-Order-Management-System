"""Order service containing business logic."""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.core import (
    InsufficientInventoryException,
    OrderNotFoundException,
    CustomerNotFoundException,
    InvalidOrderItemsException,
    ProductNotFoundException,
)
from app.modules.customers.customer_repository import CustomerRepository
from app.modules.products.product_repository import ProductRepository

from .order_item_model import OrderItem
from .order_model import Order, OrderStatus
from .order_repository import OrderRepository
from .order_request import CreateOrderRequest


class OrderService:
    """Service layer for order operations."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.repository = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)

    def create_order(self, request: CreateOrderRequest) -> Order:
        """Create a new order with validation and inventory management."""
        # Validate customer exists
        customer = self.customer_repo.get_by_id(request.customer_id)
        if not customer:
            raise CustomerNotFoundException(request.customer_id)

        # Validate request has items
        if not request.items:
            raise InvalidOrderItemsException()

        try:
            # Check inventory and calculate total
            total_amount = Decimal("0")
            order_items_data = []

            for item_request in request.items:
                product = self.product_repo.get_by_id(item_request.product_id)
                if not product:
                    raise ProductNotFoundException(item_request.product_id)

                # Check if inventory is sufficient
                if product.quantity < item_request.quantity:
                    raise InsufficientInventoryException(
                        product_id=item_request.product_id,
                        required=item_request.quantity,
                        available=product.quantity,
                    )

                # Store data for later use
                order_items_data.append({
                    "product": product,
                    "quantity": item_request.quantity,
                    "unit_price": product.price,
                })

                # Calculate total
                total_amount += product.price * item_request.quantity

            # Create order
            order = self.repository.create(
                customer_id=request.customer_id,
                total_amount=total_amount,
                status=OrderStatus.PENDING,
            )

            # Create order items and reduce inventory
            for item_data in order_items_data:
                self.repository.create_order_item(
                    order_id=order.id,
                    product_id=item_data["product"].id,
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                )
                # Reduce inventory
                self.product_repo.reduce_stock(item_data["product"], item_data["quantity"])

            # Commit the transaction
            self.repository.commit()
            return self.repository.get_by_id(order.id)

        except Exception as e:
            # Rollback on any error
            self.repository.rollback()
            raise

    def get_order(self, order_id: int) -> Order:
        """Get order by ID."""
        order = self.repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(order_id)
        return order

    def get_all_orders(self) -> list[Order]:
        """Get all orders."""
        return self.repository.get_all()

    def delete_order(self, order_id: int) -> None:
        """Delete an order and restore reserved inventory."""
        order = self.get_order(order_id)

        try:
            for item in order.items:
                if item.product:
                    self.product_repo.increase_stock(item.product, item.quantity)

            self.repository.delete(order)
        except Exception:
            self.repository.rollback()
            raise

    def confirm_order(self, order_id: int) -> Order:
        """Confirm an order."""
        order = self.get_order(order_id)
        return self.repository.update_status(order, OrderStatus.CONFIRMED)

    def cancel_order(self, order_id: int) -> Order:
        """Cancel an order."""
        order = self.get_order(order_id)
        return self.repository.update_status(order, OrderStatus.CANCELLED)
