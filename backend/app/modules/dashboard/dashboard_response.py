"""Dashboard response schemas for API responses."""

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    """Response schema for dashboard summary."""

    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products_count: int
    low_stock_threshold: int = 5

    class Config:
        json_schema_extra = {
            "example": {
                "total_products": 50,
                "total_customers": 30,
                "total_orders": 100,
                "low_stock_products_count": 5,
                "low_stock_threshold": 5,
            }
        }
