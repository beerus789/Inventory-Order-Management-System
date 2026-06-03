"""Global exception handlers for FastAPI."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import AppException
from .response import error_response
from .status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from .error_codes import INTERNAL_SERVER_ERROR


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.message,
            error_code=exc.error_code,
            details=exc.details,
        ).dict(),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="An unexpected error occurred",
            error_code=INTERNAL_SERVER_ERROR,
        ).dict(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
