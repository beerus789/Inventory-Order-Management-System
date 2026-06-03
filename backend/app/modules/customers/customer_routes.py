"""Customer API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from .customer_request import CreateCustomerRequest, UpdateCustomerRequest
from .customer_response import CustomerResponse, CustomerListResponse
from .customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    request: CreateCustomerRequest,
    db: Session = Depends(get_db),
):
    """Create a new customer."""
    service = CustomerService(db)
    customer = service.create_customer(
        name=request.name,
        email=request.email,
        phone=request.phone,
    )
    return customer


@router.get("", response_model=CustomerListResponse)
def get_all_customers(db: Session = Depends(get_db)):
    """Retrieve all customers."""
    service = CustomerService(db)
    customers = service.get_all_customers()
    return CustomerListResponse(items=customers, total=len(customers))


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Retrieve customer details by ID."""
    service = CustomerService(db)
    return service.get_customer(customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    request: UpdateCustomerRequest,
    db: Session = Depends(get_db),
):
    """Update customer details."""
    service = CustomerService(db)
    return service.update_customer(
        customer_id=customer_id,
        name=request.name,
        phone=request.phone,
    )


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer."""
    service = CustomerService(db)
    service.delete_customer(customer_id)
    return None
