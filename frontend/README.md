# Inventory & Order Management System - Frontend

A modern, responsive React frontend for managing inventory, customers, and orders. Built with Vite, React Router, and Axios for seamless integration with the FastAPI backend.

## Features

✨ **Dashboard** - Overview of total products, customers, orders, and low-stock alerts
📦 **Products** - Create, read, update, and delete products with inventory tracking
👥 **Customers** - Manage customer information with email validation
📋 **Orders** - Create complex orders with multiple products and track order status
📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
🎨 **Modern UI** - Clean, professional dashboard-style interface
⚡ **Fast Performance** - Built with Vite for lightning-fast development and production builds

## Tech Stack

- **React 18** - UI library
- **Vite** - Next-generation frontend build tool
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API calls
- **Plain CSS** - No build dependencies for styling
- **Docker & Nginx** - Production-ready containerization

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── axios.js                 # Axios instance with base configuration
│   │   ├── productApi.js            # Product API endpoints
│   │   ├── customerApi.js           # Customer API endpoints
│   │   └── orderApi.js              # Order API endpoints
│   ├── components/
│   │   ├── Layout.jsx               # Main layout wrapper
│   │   ├── Navbar.jsx               # Top navigation bar
│   │   ├── Sidebar.jsx              # Left sidebar navigation
│   │   ├── SummaryCard.jsx          # Dashboard card component
│   │   ├── Loading.jsx              # Loading spinner
│   │   ├── Alert.jsx                # Alert/notification component
│   │   └── ConfirmDialog.jsx        # Confirmation modal
│   ├── pages/
│   │   ├── Dashboard.jsx            # Dashboard page
│   │   ├── Products.jsx             # Products management page
│   │   ├── Customers.jsx            # Customers management page
│   │   ├── Orders.jsx               # Orders list page
│   │   └── OrderDetails.jsx         # Order details page
│   ├── styles/
│   │   └── global.css               # Global styles (2000+ lines)
│   ├── App.jsx                      # Main app component with routing
│   └── main.jsx                     # React entry point
├── public/                          # Static assets
├── index.html                       # HTML entry point
├── vite.config.js                   # Vite configuration
├── package.json                     # Dependencies and scripts
├── Dockerfile                       # Multi-stage Docker build
├── nginx.conf                       # Nginx configuration
├── .dockerignore                    # Docker ignore file
├── .env                             # Environment variables
└── README.md                        # This file
```

## Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
```

For Docker deployment, adjust the URL to your backend host:

```env
VITE_API_BASE_URL=http://backend:8000
```

## Installation & Local Development

### Prerequisites

- Node.js 16+ and npm (or yarn/pnpm)
- Backend API running at `http://localhost:8000`

### Setup

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env if needed (default is already localhost:8000)
   ```

3. **Start development server:**

   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

4. **Build for production:**

   ```bash
   npm run build
   ```

   Output will be in the `dist/` directory.

5. **Preview production build:**

   ```bash
   npm run preview
   ```

## API Integration

All API calls go through the centralized Axios instance configured in `src/api/axios.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### API Endpoints Used

**Products:**
- `POST /products` - Create product
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

**Customers:**
- `POST /customers` - Create customer
- `GET /customers` - List all customers
- `GET /customers/{id}` - Get customer details
- `DELETE /customers/{id}` - Delete customer

**Orders:**
- `POST /orders` - Create order
- `GET /orders` - List all orders
- `GET /orders/{id}` - Get order details
- `DELETE /orders/{id}` - Delete order

## Docker Deployment

### Build Docker Image

```bash
docker build -t inventory-frontend:latest .
```

### Run Container Locally

```bash
docker run -p 80:80 \
  -e VITE_API_BASE_URL=http://localhost:8000 \
  inventory-frontend:latest
```

Access at `http://localhost`

### Docker Compose

Add to your `docker-compose.yml`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  container_name: inventory_frontend
  ports:
    - "80:80"
  environment:
    VITE_API_BASE_URL: http://backend:8000
  depends_on:
    - backend
  networks:
    - inventory_network
```

Note: Environment variables must be set at **build time** with Vite. For Docker, rebuild the image with the correct `VITE_API_BASE_URL` value.

## Key Features & Implementation

### Dashboard
- Real-time statistics from backend API
- Summary cards showing total products, customers, orders
- Low-stock alert system (quantity ≤ 5)
- Error handling and loading states

### Products Page
- Full CRUD operations
- Inline form for adding/editing products
- Stock status indicator
- Price and quantity validation
- Low-stock visual indicators

### Customers Page
- Create and manage customers
- Email format validation
- Delete functionality with confirmation
- Responsive table layout

### Orders Page
- Create complex orders with multiple products
- Customer dropdown selection
- Dynamic product selection
- Quantity management
- Order list with summary
- Delete with confirmation

### Order Details Page
- Full order information display
- Customer details
- Itemized breakdown
- Calculated totals
- Order status tracking

### UI/UX Features
- Responsive sidebar navigation
- Breadcrumb-style navigation
- Loading spinners for async operations
- Toast-style alerts for success/error messages
- Confirmation dialogs before destructive actions
- Empty states when no data exists
- Mobile-optimized tables and forms
- Smooth animations and transitions
- Color-coded status indicators

## Styling

The frontend uses a comprehensive CSS file (`src/styles/global.css`) with:
- Modern color scheme with gradients
- Flexbox and CSS Grid layouts
- Responsive design breakpoints
- Reusable component styles
- Smooth transitions and animations
- Accessible form inputs
- Professional button styles
- Mobile-first approach

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development Workflows

### Adding a New Page

1. Create `src/pages/YourPage.jsx`
2. Import in `src/App.jsx`
3. Add route: `<Route path="/your-page" element={<YourPage />} />`
4. Add nav link in `src/components/Sidebar.jsx`
5. Import API functions from `src/api/`
6. Use `Layout` component and style with existing classes

### Adding a New API Endpoint

1. Create function in corresponding `src/api/*.js` file
2. Use `apiClient.get|post|put|delete(path)`
3. Handle errors with try/catch
4. Show user feedback via Alert component

### Styling Components

- Use global CSS classes from `src/styles/global.css`
- Add inline styles for component-specific needs
- Use CSS Grid/Flexbox for layouts
- Mobile breakpoints: 768px, 480px

## Error Handling

All pages include:
- Try/catch blocks for API calls
- User-friendly error messages
- Error alert display
- Loading state management
- Automatic alert dismissal

## Performance Optimizations

- Vite for fast HMR during development
- Optimized CSS with reusable classes
- Efficient component re-renders
- Lazy loading routes (can be added)
- Image/asset optimization in production
- Gzip compression via Nginx
- Cache-Control headers for static assets

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running at `VITE_API_BASE_URL`
- Check CORS headers on backend API
- Verify environment variable is correct

### "Build fails with import errors"
- Clear `node_modules` and `dist`
- Run `npm install` again
- Check for circular imports

### "Styles not loading"
- Clear browser cache
- Verify `global.css` is imported in `main.jsx`
- Check network tab for 404 errors

### "Docker build fails"
- Ensure `node_modules` is in `.dockerignore`
- Check for correct `package-lock.json`
- Verify Node version compatibility

## Production Deployment

### Vercel

1. Push code to GitHub
2. Connect repository in Vercel dashboard
3. Set environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend-domain.com
   ```
4. Deploy with `npm run build` command

### Netlify

1. Push code to GitHub
2. Connect repository in Netlify dashboard
3. Set build command: `npm run build`
4. Set publish directory: `dist`
5. Add environment variable: `VITE_API_BASE_URL`

### Self-hosted with Docker

```bash
docker build -t inventory-frontend:1.0 .
docker push your-registry/inventory-frontend:1.0
docker run -p 80:80 your-registry/inventory-frontend:1.0
```

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Test locally: `npm run dev`
4. Build: `npm run build`
5. Submit pull request

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API endpoints compatibility
3. Check browser console for errors
4. Verify backend API is responding correctly

---

Built with ❤️ for efficient inventory management
