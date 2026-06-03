"""Custom exception classes for the application."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception class for all application exceptions."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ProductNotFoundException(AppException):
    """Raised when a product is not found."""

    def __init__(self, product_id: int):
        from .error_codes import PRODUCT_NOT_FOUND
        from .status_codes import HTTP_404_NOT_FOUND

        super().__init__(
            message=f"Product with ID {product_id} not found",
            error_code=PRODUCT_NOT_FOUND,
            status_code=HTTP_404_NOT_FOUND,
            details={"product_id": product_id},
        )


class ProductSKUAlreadyExistsException(AppException):
    """Raised when a product SKU already exists."""

    def __init__(self, sku: str):
        from .error_codes import PRODUCT_SKU_ALREADY_EXISTS
        from .status_codes import HTTP_409_CONFLICT

        super().__init__(
            message=f"Product with SKU '{sku}' already exists",
            error_code=PRODUCT_SKU_ALREADY_EXISTS,
            status_code=HTTP_409_CONFLICT,
            details={"sku": sku},
        )


class InvalidProductPriceException(AppException):
    """Raised when product price is invalid."""

    def __init__(self, price: float):
        from .error_codes import INVALID_PRODUCT_PRICE
        from .status_codes import HTTP_400_BAD_REQUEST

        super().__init__(
            message="Product price must be greater than or equal to zero",
            error_code=INVALID_PRODUCT_PRICE,
            status_code=HTTP_400_BAD_REQUEST,
            details={"price": price},
        )


class InvalidProductQuantityException(AppException):
    """Raised when product quantity is invalid."""

    def __init__(self, quantity: int):
        from .error_codes import INVALID_PRODUCT_QUANTITY
        from .status_codes import HTTP_400_BAD_REQUEST

        super().__init__(
            message="Product quantity cannot be negative",
            error_code=INVALID_PRODUCT_QUANTITY,
            status_code=HTTP_400_BAD_REQUEST,
            details={"quantity": quantity},
        )


class CustomerNotFoundException(AppException):
    """Raised when a customer is not found."""

    def __init__(self, customer_id: int):
        from .error_codes import CUSTOMER_NOT_FOUND
        from .status_codes import HTTP_404_NOT_FOUND

        super().__init__(
            message=f"Customer with ID {customer_id} not found",
            error_code=CUSTOMER_NOT_FOUND,
            status_code=HTTP_404_NOT_FOUND,
            details={"customer_id": customer_id},
        )


class CustomerEmailAlreadyExistsException(AppException):
    """Raised when a customer email already exists."""

    def __init__(self, email: str):
        from .error_codes import CUSTOMER_EMAIL_ALREADY_EXISTS
        from .status_codes import HTTP_409_CONFLICT

        super().__init__(
            message=f"Customer with email '{email}' already exists",
            error_code=CUSTOMER_EMAIL_ALREADY_EXISTS,
            status_code=HTTP_409_CONFLICT,
            details={"email": email},
        )


class InvalidCustomerEmailException(AppException):
    """Raised when customer email is invalid."""

    def __init__(self, email: str):
        from .error_codes import INVALID_CUSTOMER_EMAIL
        from .status_codes import HTTP_422_UNPROCESSABLE_ENTITY

        super().__init__(
            message="Invalid email format",
            error_code=INVALID_CUSTOMER_EMAIL,
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            details={"email": email},
        )


class InvalidCustomerPhoneException(AppException):
    """Raised when customer phone is invalid."""

    def __init__(self, phone: str):
        from .error_codes import INVALID_CUSTOMER_PHONE
        from .status_codes import HTTP_422_UNPROCESSABLE_ENTITY

        super().__init__(
            message="Invalid phone number format",
            error_code=INVALID_CUSTOMER_PHONE,
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            details={"phone": phone},
        )


class OrderNotFoundException(AppException):
    """Raised when an order is not found."""

    def __init__(self, order_id: int):
        from .error_codes import ORDER_NOT_FOUND
        from .status_codes import HTTP_404_NOT_FOUND

        super().__init__(
            message=f"Order with ID {order_id} not found",
            error_code=ORDER_NOT_FOUND,
            status_code=HTTP_404_NOT_FOUND,
            details={"order_id": order_id},
        )


class InsufficientInventoryException(AppException):
    """Raised when there is insufficient inventory for an order."""

    def __init__(self, product_id: int, required: int, available: int):
        from .error_codes import INSUFFICIENT_INVENTORY
        from .status_codes import HTTP_409_CONFLICT

        super().__init__(
            message=f"Insufficient inventory. Required: {required}, Available: {available}",
            error_code=INSUFFICIENT_INVENTORY,
            status_code=HTTP_409_CONFLICT,
            details={
                "product_id": product_id,
                "required": required,
                "available": available,
            },
        )


class InvalidOrderItemsException(AppException):
    """Raised when order items are invalid."""

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        from .error_codes import INVALID_ORDER_ITEMS
        from .status_codes import HTTP_400_BAD_REQUEST

        super().__init__(
            message="Order must contain at least one item",
            error_code=INVALID_ORDER_ITEMS,
            status_code=HTTP_400_BAD_REQUEST,
            details=details,
        )
