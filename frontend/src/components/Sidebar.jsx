import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <div className="sidebar">
      <div className="sidebar-title">
        <span className="brand-mark">I</span>
        <span className="brand-copy">
          Inventory
          <small>Order manager</small>
        </span>
      </div>
      <nav className="sidebar-nav">
        <Link to="/" className={`nav-link ${isActive('/')}`}>
          <span className="nav-icon">D</span>
          <span>Dashboard</span>
        </Link>
        <Link to="/products" className={`nav-link ${isActive('/products')}`}>
          <span className="nav-icon">P</span>
          <span>Products</span>
        </Link>
        <Link to="/customers" className={`nav-link ${isActive('/customers')}`}>
          <span className="nav-icon">C</span>
          <span>Customers</span>
        </Link>
        <Link to="/orders" className={`nav-link ${isActive('/orders')}`}>
          <span className="nav-icon">O</span>
          <span>Orders</span>
        </Link>
      </nav>
    </div>
  );
}

export default Sidebar;
