"""Customer repository for database operations."""

from typing import Optional

from sqlalchemy.orm import Session

from .customer_model import Customer


class CustomerRepository:
    """Repository for customer database operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, name: str, email: str, phone: str) -> Customer:
        """Create a new customer."""
        customer = Customer(name=name, email=email, phone=phone)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        return self.db.query(Customer).filter(Customer.email == email.lower()).first()

    def get_all(self) -> list[Customer]:
        """Get all customers."""
        return self.db.query(Customer).all()

    def update(self, customer: Customer, **kwargs) -> Customer:
        """Update customer fields."""
        for key, value in kwargs.items():
            if value is not None and hasattr(customer, key):
                setattr(customer, key, value)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer: Customer) -> None:
        """Delete a customer."""
        self.db.delete(customer)
        self.db.commit()
