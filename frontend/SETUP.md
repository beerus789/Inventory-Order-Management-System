# Frontend Setup & Deployment Guide

## Quick Start

### Local Development (No Docker)

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Ensure backend is running at http://localhost:8000
# (Backend should be running in another terminal or Docker container)

# 3. Start development server
npm run dev

# App opens at http://localhost:3000
```

### Local Development with Docker Compose

```bash
# From the assignment root directory
docker-compose up

# Access:
# - Frontend: http://localhost
# - Backend API: http://localhost:8000
# - Database: localhost:5432
```

## Building for Production

### Option 1: Build Locally, Deploy Manually

```bash
cd frontend

# Build the app
npm run build

# Output is in dist/ folder
# Can be deployed to any static hosting (Vercel, Netlify, S3, etc.)
```

### Option 2: Docker Image

```bash
# Build frontend image
docker build -t inventory-frontend:latest ./frontend

# Run standalone
docker run -p 80:80 \
  -e VITE_API_BASE_URL=http://your-backend-url:8000 \
  inventory-frontend:latest

# Or use with docker-compose for full stack
docker-compose up --build
```

## Environment Configuration

### Local Development
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Docker Compose
```env
VITE_API_BASE_URL=http://backend:8000
```

### Production (Deployed Backend)
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Project Features

### Pages Implemented

#### 1. Dashboard (`/`)
- **Summary Cards**: Total products, customers, orders, low-stock count
- **Real-time Stats**: Fetches from backend API
- **Quick Stats Section**: Welcome message and navigation tips

#### 2. Products (`/products`)
- **View**: Table with all products
- **Create**: Form to add new products
- **Edit**: Inline edit functionality
- **Delete**: With confirmation dialog
- **Validation**: 
  - Required fields (name, SKU, price, quantity)
  - Price ≥ 0
  - Quantity ≥ 0
  - Low stock indicator (≤ 5)
- **Stock Status**: Visual indicator for low/in stock

#### 3. Customers (`/customers`)
- **View**: Table with all customers
- **Create**: Form to add customers
- **Delete**: With confirmation dialog
- **Validation**:
  - Required fields (name, email, phone)
  - Email format validation
- **Form States**: Collapsed/expanded toggle

#### 4. Orders (`/orders`)
- **View**: List of all orders with status
- **Create**: Multi-product order creation
- **Features**:
  - Customer dropdown selection
  - Multiple product addition
  - Dynamic quantity input
  - Order summary with total amount
  - Add/remove item functionality
  - Quantity validation (≥ 1)
- **Delete**: With confirmation dialog

#### 5. Order Details (`/orders/:id`)
- **Display Order Info**: ID, status, date, total
- **Customer Information**: Name, email, phone
- **Order Items**: Complete breakdown with prices
- **Back Navigation**: Return to orders list
- **Delete Option**: Remove order from details page

### Component Library

#### Layout Components
- **Layout**: Main wrapper with sidebar and content area
- **Sidebar**: Navigation menu with active state highlighting
- **Navbar**: Top bar showing current page title

#### UI Components
- **SummaryCard**: Dashboard stat card with gradients
- **Loading**: Spinner component for async operations
- **Alert**: Auto-dismissing notification for success/error/warning
- **ConfirmDialog**: Modal for destructive actions
- **Tables**: Responsive table with hover effects
- **Forms**: Controlled inputs with validation
- **Buttons**: Multiple variants (primary, success, danger, warning)
- **Empty States**: Helpful messages when no data exists

### API Integration

All API calls use a centralized Axios instance:

```javascript
// src/api/axios.js
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});
```

#### API Functions

**productApi.js**
- `getProducts()` - Fetch all products
- `getProductById(id)` - Fetch single product
- `createProduct(data)` - Create new product
- `updateProduct(id, data)` - Update product
- `deleteProduct(id)` - Delete product

**customerApi.js**
- `getCustomers()` - Fetch all customers
- `getCustomerById(id)` - Fetch single customer
- `createCustomer(data)` - Create new customer
- `deleteCustomer(id)` - Delete customer

**orderApi.js**
- `getOrders()` - Fetch all orders
- `getOrderById(id)` - Fetch single order
- `createOrder(data)` - Create new order
- `deleteOrder(id)` - Delete order

### Styling System

**global.css** (2000+ lines) includes:
- CSS variables for colors
- Responsive grid system
- Component styles
- Animations and transitions
- Dark/light color schemes
- Mobile-first approach
- Accessibility features

**Breakpoints:**
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 480px - 767px
- Small Mobile: < 480px

## Scripts

```bash
npm run dev        # Start Vite dev server (port 3000)
npm run build      # Build for production (creates dist/)
npm run preview    # Preview production build locally
```

## Troubleshooting

### Frontend won't connect to backend
1. Check `VITE_API_BASE_URL` in `.env`
2. Ensure backend is running: `curl http://localhost:8000/docs`
3. Check CORS settings on backend
4. Clear browser cache and reload

### Build fails
1. Delete `node_modules` and `dist`
2. Run `npm install` again
3. Run `npm run build`

### Port already in use
```bash
# Change dev port in vite.config.js
# Or kill process on port 3000:
lsof -ti:3000 | xargs kill -9
```

### Docker issues
1. Rebuild image: `docker build --no-cache -t inventory-frontend:latest ./frontend`
2. Clear volumes: `docker-compose down -v`
3. Rebuild everything: `docker-compose up --build`

## Deployment Platforms

### Vercel
```bash
npm i -g vercel
vercel env add VITE_API_BASE_URL https://api.yourdomain.com
vercel
```

### Netlify
1. Connect GitHub repo in Netlify dashboard
2. Build command: `npm run build`
3. Publish directory: `dist`
4. Environment: Set `VITE_API_BASE_URL`

### AWS Amplify
```bash
npm i -g @aws-amplify/cli
amplify init
amplify publish
```

### Self-hosted
```bash
npm run build
# Upload dist/ contents to web server
# Configure web server to serve index.html for all routes
```

## Performance Tips

1. **Images**: Optimize before adding
2. **Code splitting**: React Router enables this automatically
3. **Caching**: Nginx config handles static assets
4. **Gzip**: Enabled in nginx.conf
5. **Tree-shaking**: Vite handles automatically

## Security Considerations

1. **Never commit .env with secrets**: Use .env.example template
2. **CORS**: Backend must allow frontend origin
3. **API Key**: Never hardcode in frontend (would be visible)
4. **Input validation**: Implement on both frontend and backend
5. **HTTPS**: Use in production
6. **XSS Prevention**: React escapes by default

## Monitoring & Debugging

### Browser DevTools
- React DevTools extension
- Network tab for API calls
- Console for errors
- Application tab for storage

### Backend Logs
```bash
docker logs inventory_backend
```

### Database
```bash
docker exec -it inventory_db psql -U postgres -d inventory_db
```

## File Reference

```
frontend/
├── src/
│   ├── api/                 # API client functions
│   ├── components/          # Reusable UI components
│   ├── pages/               # Page components
│   ├── styles/global.css    # All styling
│   ├── App.jsx              # Routing setup
│   └── main.jsx             # Entry point
├── public/                  # Static assets
├── Dockerfile               # Multi-stage Docker build
├── nginx.conf               # Nginx server config
├── vite.config.js           # Vite configuration
├── package.json             # Dependencies
├── .env                     # Environment variables
├── .dockerignore             # Docker ignore rules
└── README.md                # Full documentation
```

## Next Steps

1. Install dependencies: `npm install`
2. Start dev server: `npm run dev`
3. Test all pages
4. Verify backend API calls work
5. Build for production: `npm run build`
6. Deploy to your chosen platform

---

For more details, see README.md in the frontend directory.
