"""Customer request schemas for API validation."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateCustomerRequest(BaseModel):
    """Request schema for creating a customer."""

    name: str = Field(..., min_length=1, max_length=255, description="Customer full name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: str = Field(..., min_length=10, max_length=20, description="Customer phone number")

    @field_validator("name")
    @classmethod
    def name_strip(cls, v: str) -> str:
        """Strip whitespace from name."""
        return v.strip()

    @field_validator("phone")
    @classmethod
    def phone_strip(cls, v: str) -> str:
        """Strip whitespace and validate phone."""
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-234-567-8900",
            }
        }


class UpdateCustomerRequest(BaseModel):
    """Request schema for updating a customer."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)

    @field_validator("name")
    @classmethod
    def name_strip(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from name."""
        return v.strip() if v else None

    @field_validator("phone")
    @classmethod
    def phone_strip(cls, v: Optional[str]) -> Optional[str]:
        """Strip whitespace from phone."""
        return v.strip() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "phone": "+1-234-567-8901",
            }
        }
