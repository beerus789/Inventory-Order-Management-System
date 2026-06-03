# Quick Start Guide

## TL;DR - Get Running in 5 Minutes

### With Docker (Recommended)

```bash
# 1. Navigate to backend directory
cd backend

# 2. Copy environment file
cp .env.example .env

# 3. Start everything with Docker Compose
docker-compose up --build

# 4. Wait for containers to start (should see "Application startup complete")

# 5. Visit http://localhost:8000/docs for interactive API docs
```

That's it! Your API is running.

### Without Docker

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Can't able to activate venv then run the below cmd present in 35 and 36 line
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
cp .env.example .env
# Edit .env to match your local PostgreSQL setup

# 5. Create database
createdb -U postgres inventory_db

# 6. Run migrations
alembic upgrade head

# 7. Start server
uvicorn app.main:app --reload

# 8. Visit http://localhost:8000/docs
```

## Verify It's Working

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy", "app": "Inventory Order Management API"}
```

## Test the API

### 1. Create a Product
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

### 2. Create a Customer
```bash
curl -X POST "http://localhost:8000/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-234-567-8900"
  }'
```

### 3. Create an Order
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

### 4. Check Dashboard
```bash
curl "http://localhost:8000/dashboard/summary"
```

## API Documentation

Two ways to explore the API:

1. **Swagger UI** (Interactive): http://localhost:8000/docs
2. **ReDoc** (Alternative): http://localhost:8000/redoc

Click around, try requests directly in your browser!

## Stop the Application

### With Docker
```bash
docker-compose down
```

### Without Docker
Press `Ctrl+C` in the terminal

## Common Issues

### Port 8000 Already in Use
Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Database Connection Failed
Make sure PostgreSQL is running:
```bash
# With Docker
docker-compose logs db

# Without Docker (local PostgreSQL)
pg_isready -h localhost -U postgres
```

### Alembic Migration Issues
```bash
# Reset database (removes all data)
docker-compose down -v
docker-compose up --build
```

## Project Structure Overview

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── core/                # Shared configs & exceptions
│   ├── database/            # DB connection & models
│   └── modules/             # Products, Customers, Orders, Dashboard
├── alembic/                 # Database migrations
├── Dockerfile               # Docker image config
├── docker-compose.yml       # Docker Compose config
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # Full documentation
```

## Key Files Explained

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup & router registration |
| `app/core/` | Shared exceptions, responses, config |
| `app/modules/products/` | Product API (routes, service, models) |
| `app/modules/customers/` | Customer API |
| `app/modules/orders/` | Order API (handles inventory) |
| `app/modules/dashboard/` | Dashboard summary API |
| `alembic/` | Database schema migrations |

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **Explore API Docs**: Visit http://localhost:8000/docs
3. **Run Tests**: `pytest` or `docker-compose exec backend pytest`
4. **Check Testing Guide**: See [TESTING.md](TESTING.md)
5. **Customize**: Modify `.env` for your needs

## Architecture at a Glance

```
HTTP Request
    ↓
Routes (product_routes.py, etc.)
    ↓
Services (product_service.py) ← Business Logic
    ↓
Repositories (product_repository.py) ← Database Operations
    ↓
SQLAlchemy Models (product_model.py)
    ↓
PostgreSQL Database
```

## Important Features

✅ **Inventory Management**: Orders automatically reduce stock  
✅ **Data Validation**: All inputs validated with Pydantic  
✅ **Error Handling**: Standardized error responses with custom codes  
✅ **Transactions**: Order creation is atomic (all-or-nothing)  
✅ **Database Migrations**: Track schema changes with Alembic  
✅ **Containerization**: Run anywhere with Docker  

## Production Deployment

1. Update `.env` with production values
2. Set `APP_DEBUG=false`
3. Use production database credentials
4. Deploy Docker image to your platform

See [README.md](README.md#deployment) for details.

## Need Help?

- Check [README.md](README.md) for detailed documentation
- See [TESTING.md](TESTING.md) for test examples
- Review error codes in `app/core/error_codes.py`
- Check logs: `docker-compose logs -f backend`

Happy building! 🚀
