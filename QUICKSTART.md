# QUICKSTART - Inventory Frontend

## ⚡ Get Running in 5 Minutes

### Option 1: Local Development (Fastest)

```bash
# Terminal 1: Start the backend (if not already running)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Terminal 2: Start the frontend
cd frontend
npm install
npm run dev

# Frontend opens at http://localhost:3000
# Backend at http://localhost:8000
```

### Option 2: Docker Compose (One Command)

```bash
# From the assignment root directory
docker-compose up --build

# Wait for all services to start
# Frontend: http://localhost
# Backend: http://localhost:8000
# Database: localhost:5432
```

---

## 📂 What Was Created

```
frontend/                           # Complete React app
├── src/
│   ├── pages/                     # 5 pages (Dashboard, Products, Customers, Orders, OrderDetails)
│   ├── components/                # 7 reusable components
│   ├── api/                       # 4 API client modules
│   ├── styles/global.css          # All styling (2000+ lines)
│   └── App.jsx, main.jsx          # App setup & routing
├── Dockerfile                     # Production-ready build
├── nginx.conf                     # Web server config
├── docker-compose.yml (updated)   # For full stack
└── README.md + SETUP.md          # Full documentation
```

---

## ✅ Features Ready to Use

| Feature | Status | Location |
|---------|--------|----------|
| Dashboard | ✅ Complete | `/` |
| Products CRUD | ✅ Complete | `/products` |
| Customers CRUD | ✅ Complete | `/customers` |
| Orders Management | ✅ Complete | `/orders` |
| Order Details | ✅ Complete | `/orders/:id` |
| API Integration | ✅ Complete | `src/api/` |
| Responsive Design | ✅ Complete | `src/styles/global.css` |
| Docker Setup | ✅ Complete | `Dockerfile` + `docker-compose.yml` |

---

## 🔧 Configuration

### Development (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Docker Compose (.env)
```env
VITE_API_BASE_URL=http://backend:8000
```

### Production
```env
VITE_API_BASE_URL=https://your-api-domain.com
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete feature documentation |
| SETUP.md | Detailed setup & deployment guide |
| COMPLETION_SUMMARY.md | What was built & feature checklist |

---

## 🚀 Common Commands

```bash
# Development
npm install                 # Install dependencies
npm run dev                # Start dev server (port 3000)
npm run build              # Build for production
npm run preview            # Preview production build

# Docker
docker build -t inventory-frontend:latest .
docker run -p 80:80 inventory-frontend:latest

# Docker Compose (from root directory)
docker-compose up          # Start all services
docker-compose up --build  # Rebuild & start
docker-compose down        # Stop all services
```

---

## 📊 Pages Overview

### Dashboard (Home)
- Real-time stats from API
- Total products, customers, orders
- Low-stock alerts

### Products
- View all products in table
- Add new product (form)
- Edit existing products
- Delete with confirmation
- Stock status indicator

### Customers
- View all customers
- Add new customer (form)
- Email validation
- Delete with confirmation

### Orders
- View all orders with status
- Create order with multiple products
- Select customer from dropdown
- Add multiple items to one order
- View order details
- Delete orders

### Order Details
- Full order information
- Customer details
- Itemized products list
- Order total and status
- Delete order option

---

## 🎯 API Endpoints Used

```
Products:
  GET    /products
  POST   /products
  GET    /products/{id}
  PUT    /products/{id}
  DELETE /products/{id}

Customers:
  GET    /customers
  POST   /customers
  DELETE /customers/{id}

Orders:
  GET    /orders
  POST   /orders
  GET    /orders/{id}
  DELETE /orders/{id}
```

---

## ⚠️ Troubleshooting

### "Cannot connect to backend"
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Verify VITE_API_BASE_URL in .env
cat .env
```

### "npm: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Then reinstall dependencies
npm install
```

### "Port 3000 already in use"
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :3000   # Windows
```

### "Docker build fails"
```bash
# Clear cache and rebuild
docker build --no-cache -t inventory-frontend:latest .
```

---

## 📱 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## 🚢 Deployment

### Quick Deploy to Vercel
```bash
npm i -g vercel
vercel
```

### Quick Deploy to Netlify
1. Push code to GitHub
2. Connect repo in Netlify Dashboard
3. Set build command: `npm run build`
4. Set publish directory: `dist`

---

## 📝 Next Steps

1. **Install**: `npm install` in frontend directory
2. **Run**: `npm run dev` (frontend) + backend running
3. **Test**: Try all pages and features
4. **Build**: `npm run build` when ready
5. **Deploy**: Choose your platform

---

## 📞 Files by Purpose

**Setup & Config:**
- package.json - Dependencies
- vite.config.js - Build config
- .env - Environment variables
- Dockerfile - Container build

**Application:**
- src/App.jsx - Routing setup
- src/main.jsx - Entry point

**Pages (5 files):**
- Dashboard.jsx
- Products.jsx
- Customers.jsx
- Orders.jsx
- OrderDetails.jsx

**Components (7 files):**
- Layout, Sidebar, Navbar, SummaryCard
- Loading, Alert, ConfirmDialog

**API (4 files):**
- axios.js, productApi.js, customerApi.js, orderApi.js

**Styling:**
- src/styles/global.css (2000+ lines, everything included)

---

## ✨ Ready to Go!

Your frontend is **production-ready** with:
- ✅ All pages implemented
- ✅ Full API integration
- ✅ Responsive design
- ✅ Docker support
- ✅ Error handling
- ✅ Professional UI
- ✅ Complete documentation

**Start with `npm install` then `npm run dev` !**
