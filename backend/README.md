# Inventory and Order Management System - Backend API

A production-level FastAPI backend for managing products, customers, and orders with inventory tracking.

## Features

- ✅ Product Management (CRUD operations)
- ✅ Customer Management (CRUD operations)
- ✅ Order Management with automatic inventory tracking
- ✅ Dashboard with summary metrics
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Alembic migrations for database versioning
- ✅ Docker and Docker Compose setup
- ✅ Centralized exception handling
- ✅ Comprehensive API request validation
- ✅ Transaction-safe order creation

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose
- **Python**: 3.11

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── __init__.py
│   ├── core/                   # Shared utilities and configurations
│   │   ├── config.py           # Settings management
│   │   ├── status_codes.py     # HTTP status codes
│   │   ├── error_codes.py      # Custom error codes
│   │   ├── exceptions.py       # Custom exception classes
│   │   ├── exception_handler.py # Global exception handlers
│   │   ├── response.py         # API response formatting
│   │   └── __init__.py
│   ├── database/               # Database configuration
│   │   ├── session.py          # SQLAlchemy session setup
│   │   ├── base.py             # Base model and mixins
│   │   └── __init__.py
│   └── modules/                # Feature modules
│       ├── products/           # Product management
│       │   ├── product_model.py
│       │   ├── product_request.py
│       │   ├── product_response.py
│       │   ├── product_repository.py
│       │   ├── product_service.py
│       │   ├── product_routes.py
│       │   └── __init__.py
│       ├── customers/          # Customer management
│       │   ├── customer_model.py
│       │   ├── customer_request.py
│       │   ├── customer_response.py
│       │   ├── customer_repository.py
│       │   ├── customer_service.py
│       │   ├── customer_routes.py
│       │   └── __init__.py
│       ├── orders/             # Order management
│       │   ├── order_model.py
│       │   ├── order_item_model.py
│       │   ├── order_request.py
│       │   ├── order_response.py
│       │   ├── order_repository.py
│       │   ├── order_service.py
│       │   ├── order_routes.py
│       │   └── __init__.py
│       └── dashboard/          # Dashboard and analytics
│           ├── dashboard_response.py
│           ├── dashboard_service.py
│           ├── dashboard_routes.py
│           └── __init__.py
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_tables.py
├── alembic.ini                 # Alembic configuration
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Installation and Setup

### Prerequisites

- Docker and Docker Compose (for containerized setup)
- OR Python 3.11+ and PostgreSQL 15 (for local setup)

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository**

```bash
cd backend
```

2. **Create `.env` file from template**

```bash
cp .env.example .env
```

3. **Build and start containers**

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Option 2: Local Setup

1. **Create Python virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `.env` file from template**

```bash
cp .env.example .env
```

4. **Update database configuration in `.env`**

```
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=inventory_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

5. **Create PostgreSQL database**

```bash
createdb -U postgres inventory_db
```

6. **Run migrations**

```bash
alembic upgrade head
```

7. **Start the development server**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Health Check

```bash
curl http://localhost:8000/health
```

## API Endpoints

### Products

#### Create Product
```bash
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "sku": "LAPTOP-001",
    "price": 999.99,
    "quantity": 50
  }'
```

#### Get All Products
```bash
curl -X GET "http://localhost:8000/products"
```

#### Get Product by ID
```bash
curl -X GET "http://localhost:8000/products/1"
```

#### Update Product
```bash
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "price": 1099.99,
    "quantity": 45
  }'
```

#### Delete Product
```bash
curl -X DELETE "http://localhost:8000/products/1"
```

### Customers

#### Create Customer
```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-234-567-8900"
  }'
```

#### Get All Customers
```bash
curl -X GET "http://localhost:8000/customers"
```

#### Get Customer by ID
```bash
curl -X GET "http://localhost:8000/customers/1"
```

#### Update Customer
```bash
curl -X PUT "http://localhost:8000/customers/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "phone": "+1-234-567-8901"
  }'
```

#### Delete Customer
```bash
curl -X DELETE "http://localhost:8000/customers/1"
```

### Orders

#### Create Order
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 3
      }
    ]
  }'
```

#### Get All Orders
```bash
curl -X GET "http://localhost:8000/orders"
```

#### Get Order by ID
```bash
curl -X GET "http://localhost:8000/orders/1"
```

#### Delete Order
```bash
curl -X DELETE "http://localhost:8000/orders/1"
```

### Dashboard

#### Get Dashboard Summary
```bash
curl -X GET "http://localhost:8000/dashboard/summary"
```

Response:
```json
{
  "total_products": 50,
  "total_customers": 30,
  "total_orders": 100,
  "low_stock_products_count": 5,
  "low_stock_threshold": 5
}
```

## Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback to Previous Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

## Error Handling

The API uses standardized error responses with custom error codes.

### Error Response Format

```json
{
  "success": false,
  "message": "Error message",
  "error_code": "ERROR_CODE",
  "details": {}
}
```

### Common Error Codes

- `PRODUCT_NOT_FOUND` - Product does not exist
- `PRODUCT_SKU_ALREADY_EXISTS` - SKU is already in use
- `CUSTOMER_NOT_FOUND` - Customer does not exist
- `CUSTOMER_EMAIL_ALREADY_EXISTS` - Email is already in use
- `ORDER_NOT_FOUND` - Order does not exist
- `INSUFFICIENT_INVENTORY` - Not enough stock for order
- `INVALID_PRODUCT_PRICE` - Price validation failed
- `INVALID_PRODUCT_QUANTITY` - Quantity validation failed
- `INVALID_CUSTOMER_EMAIL` - Email format is invalid
- `INVALID_CUSTOMER_PHONE` - Phone format is invalid
- `VALIDATION_ERROR` - Request validation failed

## Testing

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app
```

## Deployment

### Production Deployment

1. Update `.env` with production values
2. Set `APP_DEBUG=false`
3. Configure `DATABASE_URL` with production database
4. Build and push Docker image:

```bash
docker build -t inventory-api:latest .
docker push your-registry/inventory-api:latest
```

5. Deploy using Docker or Kubernetes

### Environment Variables

Create a `.env` file with the following variables:

```
APP_NAME=Inventory Order Management API
APP_ENV=production
APP_DEBUG=false

DATABASE_HOST=your-db-host
DATABASE_PORT=5432
DATABASE_NAME=inventory_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-secure-password
```

## Architecture

### Layered Architecture

The application follows a clean layered architecture:

1. **Routes Layer** (`*_routes.py`)
   - Handles HTTP requests/responses
   - Route definitions and parameter validation
   - Delegates business logic to services

2. **Service Layer** (`*_service.py`)
   - Contains business logic
   - Orchestrates repository operations
   - Handles domain validation and errors

3. **Repository Layer** (`*_repository.py`)
   - Database operation abstraction
   - Manages ORM operations
   - Keeps database logic isolated

4. **Model Layer** (`*_model.py`)
   - SQLAlchemy ORM models
   - Database schema definitions

5. **Schema Layer** (`*_request.py`, `*_response.py`)
   - Pydantic validation schemas
   - Request/response serialization
   - Data validation and transformation

### Core Modules

- **Exception Handling**: Centralized custom exceptions
- **Response Formatting**: Consistent API response format
- **Configuration**: Environment-based settings
- **Database**: SQLAlchemy session management

## Performance Considerations

- Database connection pooling with SQLAlchemy
- Query optimization with proper indexing
- Decimal type for accurate financial calculations
- Transactional order creation to maintain data integrity
- Indexed fields for fast lookups (SKU, email, IDs)

## Security Considerations

- Input validation at all endpoints
- Email validation using Pydantic EmailStr
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration (configure for your domain in production)
- Environment-based secrets management

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs db
docker-compose logs backend
```

### Migration Issues

```bash
# Reset database (development only)
docker-compose down -v
docker-compose up --build
```

### Port Already in Use

Change ports in `docker-compose.yml` or use:

```bash
docker-compose up -p my-project
```

## Future Enhancements

- [ ] Authentication and authorization
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] Advanced search and filtering
- [ ] File uploads for products
- [ ] Order status notifications
- [ ] Inventory forecasting
- [ ] Analytics and reporting
- [ ] Payment integration
- [ ] Multi-warehouse support

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue in the repository.

---

Built with ❤️ using FastAPI and PostgreSQL
