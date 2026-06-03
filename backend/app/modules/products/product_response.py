"""Product response schemas for API responses."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductResponse(BaseModel):
    """Response schema for a product."""

    id: int
    name: str
    sku: str
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "sku": "LAPTOP-001",
                "price": "999.99",
                "quantity": 50,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
            }
        }


class ProductListResponse(BaseModel):
    """Response schema for product list."""

    items: list[ProductResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "Laptop",
                        "sku": "LAPTOP-001",
                        "price": "999.99",
                        "quantity": 50,
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00",
                    }
                ],
                "total": 1,
            }
        }
