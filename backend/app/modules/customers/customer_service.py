"""Customer service containing business logic."""

from sqlalchemy.orm import Session

from app.core import (
    CustomerEmailAlreadyExistsException,
    CustomerNotFoundException,
)

from .customer_model import Customer
from .customer_repository import CustomerRepository


class CustomerService:
    """Service layer for customer operations."""

    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.repository = CustomerRepository(db)

    def create_customer(self, name: str, email: str, phone: str) -> Customer:
        """Create a new customer with validation."""
        # Check if email already exists
        existing = self.repository.get_by_email(email)
        if existing:
            raise CustomerEmailAlreadyExistsException(email)

        return self.repository.create(name, email, phone)

    def get_customer(self, customer_id: int) -> Customer:
        """Get customer by ID."""
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException(customer_id)
        return customer

    def get_all_customers(self) -> list[Customer]:
        """Get all customers."""
        return self.repository.get_all()

    def update_customer(
        self, customer_id: int, name: str = None, phone: str = None
    ) -> Customer:
        """Update customer."""
        customer = self.get_customer(customer_id)
        return self.repository.update(customer, name=name, phone=phone)

    def delete_customer(self, customer_id: int) -> None:
        """Delete a customer."""
        customer = self.get_customer(customer_id)
        self.repository.delete(customer)
