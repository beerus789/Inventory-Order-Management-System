"""Customer response schemas for API responses."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class CustomerResponse(BaseModel):
    """Response schema for a customer."""

    id: int
    name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-234-567-8900",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
            }
        }


class CustomerListResponse(BaseModel):
    """Response schema for customer list."""

    items: list[CustomerResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "phone": "+1-234-567-8900",
                        "created_at": "2024-01-01T10:00:00",
                        "updated_at": "2024-01-01T10:00:00",
                    }
                ],
                "total": 1,
            }
        }
