"""Dashboard service containing business logic."""

from sqlalchemy.orm import Session

from app.modules.products.product_service import ProductService
from app.modules.customers.customer_service import CustomerService
from app.modules.orders.order_service import OrderService


class DashboardService:
    """Service layer for dashboard operations."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.product_service = ProductService(db)
        self.customer_service = CustomerService(db)
        self.order_service = OrderService(db)

    def get_summary(self, low_stock_threshold: int = 5) -> dict:
        """Get dashboard summary."""
        # Get counts
        total_products = len(self.product_service.get_all_products())
        total_customers = len(self.customer_service.get_all_customers())
        total_orders = len(self.order_service.get_all_orders())

        # Get low stock products
        low_stock_products = self.product_service.get_low_stock_products(low_stock_threshold)
        low_stock_count = len(low_stock_products)

        return {
            "total_products": total_products,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "low_stock_products_count": low_stock_count,
            "low_stock_threshold": low_stock_threshold,
        }
