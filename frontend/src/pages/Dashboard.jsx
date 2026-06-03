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

  if (loading) {
    return (
      <Layout title="Dashboard">
        <Loading />
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard">
      <div className="page-stack">
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
            note="Catalog items"
          />
          <SummaryCard
            title="Total Customers"
            value={stats.totalCustomers}
            className="customers"
            note="Buyer records"
          />
          <SummaryCard
            title="Total Orders"
            value={stats.totalOrders}
            className="orders"
            note="Order history"
          />
          <SummaryCard
            title="Low Stock"
            value={stats.lowStockProducts}
            className="low-stock"
            note="Needs attention"
          />
        </div>

        <div className="card">
          <div className="card-header">
            <h2>Inventory Snapshot</h2>
          </div>
          <div className="panel-copy">
            <div className="panel-kicker">Live workspace</div>
            <h3>Stock, buyers, and orders in one responsive console.</h3>
            <p>
              The dashboard highlights catalog size, customer activity, order volume,
              and stock risk so the next action is easy to spot.
            </p>
            <div className="metric-strip">
              <div className="metric-item">
                <span>Stock risk</span>
                <strong>{stats.lowStockProducts}</strong>
              </div>
              <div className="metric-item">
                <span>Customers</span>
                <strong>{stats.totalCustomers}</strong>
              </div>
              <div className="metric-item">
                <span>Orders</span>
                <strong>{stats.totalOrders}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;
