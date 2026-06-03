import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import SummaryCard from '../components/SummaryCard';
import Loading from '../components/Loading';
import Alert from '../components/Alert';
import { getProducts } from '../api/productApi';
import { getCustomers } from '../api/customerApi';
import { getOrders } from '../api/orderApi';

function Dashboard() {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalCustomers: 0,
    totalOrders: 0,
    lowStockProducts: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [productsRes, customersRes, ordersRes] = await Promise.all([
        getProducts(),
        getCustomers(),
        getOrders(),
      ]);

      const products = productsRes.data?.data || productsRes.data || [];
      const customers = customersRes.data?.data || customersRes.data || [];
      const orders = ordersRes.data?.data || ordersRes.data || [];

      // Find low stock products (quantity <= 5)
      const lowStockCount = products.filter(
        (p) => (p.quantity_in_stock || p.quantity || 0) <= 5
      ).length;

      setStats({
        totalProducts: products.length,
        totalCustomers: customers.length,
        totalOrders: orders.length,
        lowStockProducts: lowStockCount,
      });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Layout title="Dashboard"><Loading /></Layout>;

  return (
    <Layout title="Dashboard">
      <div>
        {error && (
          <Alert
            type="error"
            message={error}
            onClose={() => setError(null)}
          />
        )}

        <div className="summary-cards">
          <SummaryCard
            title="Total Products"
            value={stats.totalProducts}
            className="products"
          />
          <SummaryCard
            title="Total Customers"
            value={stats.totalCustomers}
            className="customers"
          />
          <SummaryCard
            title="Total Orders"
            value={stats.totalOrders}
            className="orders"
          />
          <SummaryCard
            title="Low Stock Products"
            value={stats.lowStockProducts}
            className="low-stock"
          />
        </div>

        <div className="card">
          <div className="card-header">
            <h2>Quick Stats</h2>
          </div>
          <div style={{ padding: '20px' }}>
            <p>👋 Welcome to the Inventory & Order Management System</p>
            <p style={{ marginTop: '12px', color: '#7f8c8d', fontSize: '14px' }}>
              Use the navigation menu on the left to manage products, customers, and orders. 
              Keep track of low stock items to ensure inventory levels are adequate.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;
