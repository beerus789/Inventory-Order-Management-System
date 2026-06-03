"""Product API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core import success_response
from app.database import get_db

from .product_request import CreateProductRequest, UpdateProductRequest
from .product_response import ProductResponse, ProductListResponse
from .product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    request: CreateProductRequest,
    db: Session = Depends(get_db),
):
    """Create a new product."""
    service = ProductService(db)
    product = service.create_product(
        name=request.name,
        sku=request.sku,
        price=request.price,
        quantity=request.quantity,
    )
    return product


@router.get("", response_model=ProductListResponse)
def get_all_products(db: Session = Depends(get_db)):
    """Retrieve all products."""
    service = ProductService(db)
    products = service.get_all_products()
    return ProductListResponse(items=products, total=len(products))


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific product by ID."""
    service = ProductService(db)
    return service.get_product(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    request: UpdateProductRequest,
    db: Session = Depends(get_db),
):
    """Update product details."""
    service = ProductService(db)
    return service.update_product(
        product_id=product_id,
        name=request.name,
        price=request.price,
        quantity=request.quantity,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product."""
    service = ProductService(db)
    service.delete_product(product_id)
    return None
