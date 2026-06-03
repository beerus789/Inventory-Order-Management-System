"""Centralized API response formatting."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response structure."""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Request processed successfully",
                "data": {},
                "error_code": None,
                "details": None,
            }
        }


class SuccessResponse(APIResponse):
    """Success API response."""

    def __init__(self, message: str = "Request processed successfully", data: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(
            success=True,
            message=message,
            data=data,
            error_code=None,
            details=None,
            **kwargs,
        )


class ErrorResponse(APIResponse):
    """Error API response."""

    def __init__(
        self,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            success=False,
            message=message,
            data=None,
            error_code=error_code,
            details=details,
            **kwargs,
        )


def success_response(
    message: str = "Request processed successfully",
    data: Optional[Dict[str, Any]] = None,
) -> SuccessResponse:
    """Create a success response."""
    return SuccessResponse(message=message, data=data)


def error_response(
    message: str,
    error_code: str,
    details: Optional[Dict[str, Any]] = None,
) -> ErrorResponse:
    """Create an error response."""
    return ErrorResponse(message=message, error_code=error_code, details=details)
