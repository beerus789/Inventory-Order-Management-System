"""Basic test examples for the Inventory Management API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# Use SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Product Tests

def test_create_product(client):
    """Test product creation."""
    response = client.post(
        "/products",
        json={
            "name": "Test Laptop",
            "sku": "LAPTOP-TEST-001",
            "price": "999.99",
            "quantity": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Laptop"
    assert data["sku"] == "LAPTOP-TEST-001"
    assert data["quantity"] == 10


def test_get_all_products(client):
    """Test retrieving all products."""
    # Create test product
    client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 5,
        },
    )

    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_product_by_id(client):
    """Test retrieving product by ID."""
    create_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 5,
        },
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"


def test_update_product(client):
    """Test updating product."""
    create_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 5,
        },
    )
    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
            "price": "150.00",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert float(data["price"]) == 150.00


def test_delete_product(client):
    """Test deleting product."""
    create_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 5,
        },
    )
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Verify product is deleted
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_duplicate_sku_error(client):
    """Test duplicate SKU error."""
    client.post(
        "/products",
        json={
            "name": "Product 1",
            "sku": "DUPLICATE-SKU",
            "price": "100.00",
            "quantity": 5,
        },
    )

    response = client.post(
        "/products",
        json={
            "name": "Product 2",
            "sku": "DUPLICATE-SKU",
            "price": "200.00",
            "quantity": 10,
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error_code"] == "PRODUCT_SKU_ALREADY_EXISTS"


# Customer Tests

def test_create_customer(client):
    """Test customer creation."""
    response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-234-567-8900",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"


def test_get_all_customers(client):
    """Test retrieving all customers."""
    client.post(
        "/customers",
        json={
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "+1-234-567-8901",
        },
    )

    response = client.get("/customers")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1


def test_duplicate_email_error(client):
    """Test duplicate email error."""
    client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-234-567-8900",
        },
    )

    response = client.post(
        "/customers",
        json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "phone": "+1-234-567-8901",
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error_code"] == "CUSTOMER_EMAIL_ALREADY_EXISTS"


# Order Tests

def test_create_order(client):
    """Test order creation."""
    # Create product
    product_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 10,
        },
    )
    product_id = product_response.json()["id"]

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-234-567-8900",
        },
    )
    customer_id = customer_response.json()["id"]

    # Create order
    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == customer_id
    assert float(data["total_amount"]) == 200.00
    assert len(data["items"]) == 1


def test_insufficient_inventory_error(client):
    """Test insufficient inventory error."""
    # Create product with low stock
    product_response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "sku": "TEST-001",
            "price": "100.00",
            "quantity": 2,
        },
    )
    product_id = product_response.json()["id"]

    # Create customer
    customer_response = client.post(
        "/customers",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-234-567-8900",
        },
    )
    customer_id = customer_response.json()["id"]

    # Try to create order with insufficient inventory
    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 10,  # More than available
                }
            ],
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error_code"] == "INSUFFICIENT_INVENTORY"


# Dashboard Tests

def test_dashboard_summary(client):
    """Test dashboard summary endpoint."""
    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_products" in data
    assert "total_customers" in data
    assert "total_orders" in data
    assert "low_stock_products_count" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
