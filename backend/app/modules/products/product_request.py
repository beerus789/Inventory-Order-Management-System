"""Product request schemas for API validation."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CreateProductRequest(BaseModel):
    """Request schema for creating a product."""

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    sku: str = Field(..., min_length=1, max_length=100, description="Product SKU/code")
    price: Decimal = Field(..., ge=0, description="Product price")
    quantity: int = Field(..., ge=0, description="Initial quantity in stock")

    @field_validator("sku")
    @classmethod
    def sku_uppercase(cls, v: str) -> str:
        """Convert SKU to uppercase."""
        return v.upper().strip()

    @field_validator("name")
    @classmethod
    def name_strip(cls, v: str) -> str:
        """Strip whitespace from name."""
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "sku": "LAPTOP-001",
                "price": "999.99",
                "quantity": 50,
            }
        }


class UpdateProductRequest(BaseModel):
    """Request schema for updating a product."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)

    @field_validator("name")
    @classmethod
    def name_strip(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from name."""
        return v.strip() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Laptop",
                "price": "1099.99",
                "quantity": 45,
            }
        }
