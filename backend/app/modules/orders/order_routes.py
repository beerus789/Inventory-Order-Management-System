"""Order API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db

from .order_request import CreateOrderRequest
from .order_response import OrderResponse, OrderListResponse
from .order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db),
):
    """Create a new order."""
    service = OrderService(db)
    order = service.create_order(request)
    return order


@router.get("", response_model=OrderListResponse)
def get_all_orders(db: Session = Depends(get_db)):
    """Retrieve all orders."""
    service = OrderService(db)
    orders = service.get_all_orders()
    return OrderListResponse(items=orders, total=len(orders))


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve order details by ID."""
    service = OrderService(db)
    return service.get_order(order_id)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete/cancel an order."""
    service = OrderService(db)
    service.delete_order(order_id)
    return None
