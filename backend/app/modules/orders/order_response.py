"""Order response schemas for API responses."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    """Response schema for order item."""

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "product_id": 1,
                "quantity": 5,
                "unit_price": "99.99",
            }
        }


class OrderResponse(BaseModel):
    """Response schema for an order."""

    id: int
    customer_id: int
    total_amount: Decimal
    status: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer_id": 1,
                "total_amount": "499.95",
                "status": "PENDING",
                "items": [
                    {
                        "id": 1,
                        "product_id": 1,
                        "quantity": 5,
                        "unit_price": "99.99",
                    }
                ],
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
            }
        }


class OrderListResponse(BaseModel):
    """Response schema for order list."""

    items: list[OrderResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "customer_id": 1,
                        "total_amount": "499.95",
                        "status": "PENDING",
                        "items": [
                            {
                                "id": 1,
                                "product_id": 1,
                                "quantity": 5,
                                "unit_price": "99.99",
                            }
                        ],
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00",
                    }
                ],
                "total": 1,
            }
        }
