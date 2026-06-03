"""Order request schemas for API validation."""

from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, field_validator


class OrderItemRequest(BaseModel):
    """Request schema for order items."""

    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 5,
            }
        }


class CreateOrderRequest(BaseModel):
    """Request schema for creating an order."""

    customer_id: int = Field(..., gt=0)
    items: List[OrderItemRequest] = Field(..., min_length=1)

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        """Validate that items list is not empty."""
        if not v:
            raise ValueError("Order must contain at least one item")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "items": [
                    {"product_id": 1, "quantity": 5},
                    {"product_id": 2, "quantity": 3},
                ],
            }
        }
