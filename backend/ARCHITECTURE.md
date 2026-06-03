# Project Structure Reference

## Complete Backend Folder Structure

```
backend/
├── alembic/
│   ├── versions/
│   │   └── 001_initial_tables.py          # Initial migration
│   ├── env.py                             # Alembic environment setup
│   └── script.py.mako                     # Migration template
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                      # Configuration management
│   │   ├── error_codes.py                 # Custom error codes
│   │   ├── exceptions.py                  # Custom exceptions
│   │   ├── exception_handler.py           # Global exception handlers
│   │   ├── response.py                    # API response formatting
│   │   └── status_codes.py                # HTTP status codes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py                        # Base model and mixins
│   │   └── session.py                     # Database session setup
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── products/
│   │   │   ├── __init__.py
│   │   │   ├── product_model.py           # SQLAlchemy model
│   │   │   ├── product_repository.py      # Data access layer
│   │   │   ├── product_request.py         # Request validation schemas
│   │   │   ├── product_response.py        # Response schemas
│   │   │   ├── product_routes.py          # API endpoints
│   │   │   └── product_service.py         # Business logic
│   │   ├── customers/
│   │   │   ├── __init__.py
│   │   │   ├── customer_model.py
│   │   │   ├── customer_repository.py
│   │   │   ├── customer_request.py
│   │   │   ├── customer_response.py
│   │   │   ├── customer_routes.py
│   │   │   └── customer_service.py
│   │   ├── orders/
│   │   │   ├── __init__.py
│   │   │   ├── order_item_model.py        # Order items model
│   │   │   ├── order_model.py
│   │   │   ├── order_repository.py
│   │   │   ├── order_request.py
│   │   │   ├── order_response.py
│   │   │   ├── order_routes.py
│   │   │   └── order_service.py           # Complex order creation logic
│   │   └── dashboard/
│   │       ├── __init__.py
│   │       ├── dashboard_response.py
│   │       ├── dashboard_routes.py
│   │       └── dashboard_service.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py                    # Test suite
│   ├── __init__.py
│   └── main.py                            # FastAPI application
├── .dockerignore                          # Docker ignore patterns
├── .env.example                           # Environment variables template
├── .gitignore                             # Git ignore patterns
├── Dockerfile                             # Docker image configuration
├── QUICK_START.md                         # Quick start guide
├── README.md                              # Full documentation
├── TESTING.md                             # Testing guide
├── alembic.ini                            # Alembic configuration
├── docker-compose.yml                     # Docker Compose configuration
└── requirements.txt                       # Python dependencies
```

## File Descriptions

### Core Module (`app/core/`)

| File | Purpose |
|------|---------|
| `config.py` | Loads environment variables and app settings using Pydantic |
| `status_codes.py` | HTTP status codes constants |
| `error_codes.py` | Custom API error codes for standardized responses |
| `exceptions.py` | Custom exception classes for domain-specific errors |
| `exception_handler.py` | Global exception handlers that convert exceptions to HTTP responses |
| `response.py` | Standard API response structures and helper functions |

### Database Module (`app/database/`)

| File | Purpose |
|------|---------|
| `session.py` | SQLAlchemy engine and session setup with dependency injection |
| `base.py` | Base model for all ORM classes and timestamp mixin |

### Product Module (`app/modules/products/`)

| File | Purpose |
|------|---------|
| `product_model.py` | SQLAlchemy ORM model for products table |
| `product_request.py` | Pydantic schemas for validating API requests |
| `product_response.py` | Pydantic schemas for API responses |
| `product_repository.py` | Data access layer for database operations |
| `product_service.py` | Business logic and validation |
| `product_routes.py` | FastAPI endpoints and request handling |

### Customer Module (`app/modules/customers/`)

Similar structure to products:
- Database model with unique email constraint
- Request/response schemas with email validation
- Repository for CRUD operations
- Service layer for business logic
- Routes for REST endpoints

### Order Module (`app/modules/orders/`)

**Additional complexity:**
- `order_item_model.py` - Relationship between orders and products
- Transactional order creation with inventory management
- Order status tracking (PENDING, CONFIRMED, CANCELLED)
- Snapshot of product prices at time of order

| File | Purpose |
|------|---------|
| `order_model.py` | Order with status and customer reference |
| `order_item_model.py` | Individual items within an order |
| `order_repository.py` | Database operations with transaction support |
| `order_service.py` | Complex logic: validation, inventory reduction, transactions |
| `order_request.py` | Request validation with items list |
| `order_response.py` | Response with order items and totals |

### Dashboard Module (`app/modules/dashboard/`)

Provides summary metrics:
- Total products, customers, orders count
- Low stock products count (threshold = 5 units)

| File | Purpose |
|------|---------|
| `dashboard_service.py` | Aggregates data from other services |
| `dashboard_response.py` | Summary statistics response schema |
| `dashboard_routes.py` | Single endpoint for dashboard data |

### Main Application (`app/main.py`)

Initializes FastAPI with:
- CORS middleware configuration
- Exception handler registration
- Router registration for all modules
- Health check endpoint
- Root endpoint

### Database Migrations (`alembic/`)

| File | Purpose |
|------|---------|
| `env.py` | Alembic environment configuration |
| `script.py.mako` | Migration file template |
| `versions/001_initial_tables.py` | Initial migration creating all tables |
| `alembic.ini` | Alembic configuration |

### Configuration Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage Docker build for production |
| `docker-compose.yml` | Orchestrates backend and PostgreSQL services |
| `.dockerignore` | Excludes unnecessary files from Docker build |
| `.env.example` | Template for environment variables |
| `.gitignore` | Git ignore patterns |
| `requirements.txt` | Python package dependencies |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive project documentation |
| `QUICK_START.md` | Get running in 5 minutes |
| `TESTING.md` | Testing guide with examples |

### Tests

| File | Purpose |
|------|---------|
| `app/tests/test_api.py` | Comprehensive test suite with examples |

## Architecture Overview

### Layered Architecture

```
HTTP Request
    ↓
routes.py (Handles HTTP, calls services)
    ↓
service.py (Business logic, validation)
    ↓
repository.py (Database operations)
    ↓
model.py (SQLAlchemy ORM)
    ↓
PostgreSQL Database
```

### Module Structure

Each module follows a consistent pattern:

```
Module/
├── __init__.py              # Exports public classes
├── {name}_model.py          # SQLAlchemy ORM
├── {name}_request.py        # Input validation
├── {name}_response.py       # Output serialization
├── {name}_repository.py     # Database layer
├── {name}_service.py        # Business logic
└── {name}_routes.py         # HTTP endpoints
```

## Database Schema

### Tables

**products**
- `id`: Primary Key
- `name`: Product name
- `sku`: Unique product code
- `price`: Decimal(10, 2)
- `quantity`: Integer
- `created_at`: Timestamp
- `updated_at`: Timestamp

**customers**
- `id`: Primary Key
- `name`: Full name
- `email`: Unique email
- `phone`: Phone number
- `created_at`: Timestamp
- `updated_at`: Timestamp

**orders**
- `id`: Primary Key
- `customer_id`: Foreign Key → customers
- `total_amount`: Decimal(12, 2)
- `status`: Enum (PENDING, CONFIRMED, CANCELLED)
- `created_at`: Timestamp
- `updated_at`: Timestamp

**order_items**
- `id`: Primary Key
- `order_id`: Foreign Key → orders
- `product_id`: Foreign Key → products
- `quantity`: Integer
- `unit_price`: Decimal(10, 2) - Snapshot of product price

### Relationships

- Customer → Orders (One-to-Many)
- Order → OrderItems (One-to-Many)
- Product → OrderItems (One-to-Many)

## Configuration Files Details

### docker-compose.yml

Services:
- **db**: PostgreSQL 15 Alpine with health checks
- **backend**: FastAPI app built from Dockerfile

Features:
- Volume for persistent database data
- Health checks for service dependencies
- Custom bridge network
- Environment variable support

### Dockerfile

Multi-stage build:
1. **Builder Stage**: Install dependencies in virtual environment
2. **Final Stage**: Copy venv and run migrations + start server

Benefits:
- Smaller final image
- Faster builds with cached layers
- Clean production image

### requirements.txt

Key packages:
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `alembic==1.12.1` - Migrations
- `pydantic==2.5.0` - Validation
- `pytest==7.4.3` - Testing

## Validation Layers

### Request Validation (`*_request.py`)

```
HTTP Request Body
    ↓
Pydantic Schema (FastAPI auto-validates)
    ↓
Service Layer (Domain validation)
    ↓
Repository Layer (Database constraints)
```

### Field Validators

- SKU: Converted to uppercase, trimmed
- Email: Validated using Pydantic EmailStr
- Phone: Length validation (10-20 chars)
- Price: Must be >= 0
- Quantity: Must be >= 0

## Error Handling Flow

```
API Route
    ↓
Validation Error? → 422 Unprocessable Entity
    ↓
Service Validation Error? → 400 Bad Request
    ↓
Business Rule Error? → 409 Conflict (duplicate SKU/email) or 404 Not Found
    ↓
Unexpected Error? → 500 Internal Server Error
    ↓
All errors → Centralized Handler → StandardResponse
```

## Deployment Considerations

### Environment-based Configuration

Settings loaded from `.env`:
- `APP_ENV`: development/production
- `APP_DEBUG`: Enable debug mode
- Database connection details
- `DATABASE_URL`: Full connection string

### Database Migrations

Run automatically on container startup:
```bash
alembic upgrade head
```

### Production Checklist

- [ ] Set `APP_DEBUG=false`
- [ ] Use production database credentials
- [ ] Configure CORS for your domain
- [ ] Set up proper logging
- [ ] Use connection pooling
- [ ] Enable HTTPS
- [ ] Set up monitoring/alerts
- [ ] Regular database backups

## Testing Strategy

Tests cover:
- ✅ CRUD operations for all modules
- ✅ Validation (duplicates, invalid data)
- ✅ Relationships (orders → products)
- ✅ Inventory management
- ✅ Error handling
- ✅ Dashboard aggregation

See `TESTING.md` for detailed testing guide.

## Key Design Decisions

1. **Decimal for Money**: Use `Decimal` instead of `float` for prices
2. **Transactional Orders**: All-or-nothing order creation
3. **Price Snapshot**: Store product price at order time
4. **Layered Architecture**: Clear separation of concerns
5. **Pydantic Validation**: Type-safe request handling
6. **Custom Exceptions**: Domain-specific error handling
7. **Repository Pattern**: Database abstraction
8. **Service Layer**: Business logic isolation

## Performance Features

- Connection pooling
- Query optimization with proper indexes
- Indexed fields: SKU, email, ID
- Efficient relationship loading
- Transaction batching in orders

## Security Features

- Input validation at all layers
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Email format validation
- Phone format validation
- Environment-based secrets (not in code)
