import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <div className="sidebar">
      <div className="sidebar-title">📦 Inventory</div>
      <nav className="sidebar-nav">
        <Link to="/" className={`nav-link ${isActive('/')}`}>
          📊 Dashboard
        </Link>
        <Link to="/products" className={`nav-link ${isActive('/products')}`}>
          📦 Products
        </Link>
        <Link to="/customers" className={`nav-link ${isActive('/customers')}`}>
          👥 Customers
        </Link>
        <Link to="/orders" className={`nav-link ${isActive('/orders')}`}>
          📋 Orders
        </Link>
      </nav>
    </div>
  );
}

export default Sidebar;
