# Testing Guide

## Running Tests

### Using pytest

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_api.py

# Run specific test
pytest app/tests/test_api.py::test_create_product
```

### Using Docker

```bash
# Run tests in container
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app
```

## Test Coverage

Current test coverage includes:

- ✅ Product CRUD operations
- ✅ Product validation (SKU uniqueness, price validation)
- ✅ Customer CRUD operations
- ✅ Customer validation (email uniqueness)
- ✅ Order creation with inventory management
- ✅ Order validation (insufficient inventory)
- ✅ Dashboard summary
- ✅ Health check endpoint

## Manual Testing with curl

### Product Management

```bash
# Create multiple products
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "sku": "LAPTOP-001", "price": 999.99, "quantity": 50}'

curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mouse", "sku": "MOUSE-001", "price": 29.99, "quantity": 200}'

curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyboard", "sku": "KEYBOARD-001", "price": 79.99, "quantity": 100}'

# Get all products
curl "http://localhost:8000/products" | jq

# Get specific product
curl "http://localhost:8000/products/1" | jq

# Update product
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 1099.99}' | jq

# Delete product
curl -X DELETE "http://localhost:8000/products/3"
```

### Customer Management

```bash
# Create multiple customers
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "phone": "+1-234-567-8900"}'

curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith", "email": "jane@example.com", "phone": "+1-234-567-8901"}'

curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob Wilson", "email": "bob@example.com", "phone": "+1-234-567-8902"}'

# Get all customers
curl "http://localhost:8000/customers" | jq

# Get specific customer
curl "http://localhost:8000/customers/1" | jq

# Update customer
curl -X PUT "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}' | jq

# Delete customer
curl -X DELETE "http://localhost:8000/customers/3"
```

### Order Management

```bash
# Create order
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 5}
    ]
  }' | jq

# Get all orders
curl "http://localhost:8000/orders" | jq

# Get specific order
curl "http://localhost:8000/orders/1" | jq

# Delete order
curl -X DELETE "http://localhost:8000/orders/1"
```

### Dashboard

```bash
# Get dashboard summary
curl "http://localhost:8000/dashboard/summary" | jq
```

## Test Scenarios

### Scenario 1: Basic CRUD Operations

1. Create a product
2. Retrieve it by ID
3. Update its details
4. Delete it

### Scenario 2: Order with Inventory Management

1. Create a product with quantity 10
2. Create a customer
3. Create an order for 5 units
4. Verify inventory reduced to 5
5. Create another order for 3 units
6. Verify inventory reduced to 2

### Scenario 3: Error Handling

1. Try creating product with duplicate SKU (expect 409)
2. Try creating customer with duplicate email (expect 409)
3. Try creating order with insufficient inventory (expect 409)
4. Try accessing non-existent product (expect 404)
5. Try accessing non-existent customer (expect 404)
6. Try accessing non-existent order (expect 404)

### Scenario 4: Dashboard Summary

1. Create 5 products
2. Create 3 customers
3. Create 2 orders
4. Create product with quantity 2 (low stock)
5. Check dashboard summary
6. Verify counts are correct

## API Response Examples

### Success Response

```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": 1,
    "name": "Laptop",
    "sku": "LAPTOP-001",
    "price": "999.99",
    "quantity": 50,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  },
  "error_code": null,
  "details": null
}
```

### Error Response

```json
{
  "success": false,
  "message": "Product with SKU 'LAPTOP-001' already exists",
  "data": null,
  "error_code": "PRODUCT_SKU_ALREADY_EXISTS",
  "details": {
    "sku": "LAPTOP-001"
  }
}
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test product list endpoint
ab -n 1000 -c 10 http://localhost:8000/products

# Test product creation
ab -n 100 -c 5 -p product.json -T application/json http://localhost:8000/products
```

### Stress Testing

```bash
# Using hey
go install github.com/rakyll/hey@latest
hey -n 10000 -c 100 http://localhost:8000/products
```

## Debugging

### Enable SQL Logging

Set `APP_DEBUG=true` in `.env` to see SQL queries:

```
APP_DEBUG=true
```

### View Logs

```bash
# Docker logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f db
```

### Database Queries

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d inventory_db

# View tables
\dt

# View products
SELECT * FROM products;

# View orders with items
SELECT o.id, o.customer_id, o.total_amount, COUNT(oi.id) as item_count
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id;
```

## Troubleshooting Tests

### Database Reset

```bash
# Reset database for clean tests
docker-compose down -v
docker-compose up --build
```

### Clear Cache

```bash
# Clear pytest cache
pytest --cache-clear

# Clear coverage
coverage erase
```

### Verbose Output

```bash
# Run tests with print statements
pytest -v -s

# Show local variables on failure
pytest -v -l
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: inventory_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          python -m pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest --cov=app
```
