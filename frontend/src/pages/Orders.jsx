import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Loading from '../components/Loading';
import Alert from '../components/Alert';
import ConfirmDialog from '../components/ConfirmDialog';
import { getOrders, createOrder, deleteOrder } from '../api/orderApi';
import { getCustomers } from '../api/customerApi';
import { getProducts } from '../api/productApi';
import { useNavigate } from 'react-router-dom';

function Orders() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [orderItems, setOrderItems] = useState([{ product_id: '', quantity: '' }]);
  const [formData, setFormData] = useState({
    customer_id: '',
  });
  const [formErrors, setFormErrors] = useState({
    customer_id: '',
    items: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [ordersRes, customersRes, productsRes] = await Promise.all([
        getOrders(),
        getCustomers(),
        getProducts(),
      ]);

      setOrders(ordersRes.data?.data || ordersRes.data || []);
      setCustomers(customersRes.data?.data || customersRes.data || []);
      setProducts(productsRes.data?.data || productsRes.data || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load data');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCustomerChange = (e) => {
    setFormData({ customer_id: e.target.value });
  };

  const handleOrderItemChange = (index, field, value) => {
    const updatedItems = [...orderItems];
    updatedItems[index][field] = value;
    setOrderItems(updatedItems);
  };

  const addOrderItem = () => {
    setOrderItems([...orderItems, { product_id: '', quantity: '' }]);
  };

  const removeOrderItem = (index) => {
    if (orderItems.length === 1) return;
    setOrderItems(orderItems.filter((_, i) => i !== index));
  };

  const resetForm = () => {
    setFormData({ customer_id: '' });
    setOrderItems([{ product_id: '', quantity: '' }]);
    setFormErrors({ customer_id: '', items: '' });
    setShowForm(false);
  };

  const validateForm = () => {
    const errors = { customer_id: '', items: '' };
    let isValid = true;

    if (!formData.customer_id) {
      errors.customer_id = 'Please select a customer';
      isValid = false;
    }

    let hasValidItems = true;
    for (const item of orderItems) {
      if (!item.product_id) {
        errors.items = 'Please select a product for all items';
        hasValidItems = false;
        break;
      }
      if (!item.quantity || parseInt(item.quantity, 10) < 1) {
        errors.items = 'All quantities must be at least 1';
        hasValidItems = false;
        break;
      }
    }

    if (!hasValidItems) {
      isValid = false;
    }

    if (orderItems.length === 0) {
      errors.items = 'Order must contain at least one item';
      isValid = false;
    }

    setFormErrors(errors);
    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) return;

    try {
      setLoading(true);

      const payload = {
        customer_id: parseInt(formData.customer_id, 10),
        items: orderItems.map((item) => ({
          product_id: parseInt(item.product_id, 10),
          quantity: parseInt(item.quantity, 10),
        })),
      };

      await createOrder(payload);
      setSuccess('Order created successfully');
      await loadData();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create order');
      console.error('Error creating order:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      setLoading(true);
      await deleteOrder(id);
      setSuccess('Order deleted successfully');
      await loadData();
      setConfirmDelete(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete order');
      console.error('Error deleting order:', err);
    } finally {
      setLoading(false);
    }
  };

  const getOrderCustomerName = (order) => {
    if (order.customer?.full_name || order.customer?.name) {
      return order.customer.full_name || order.customer.name;
    }

    const matchedCustomer = customers.find((customer) => customer.id === order.customer_id);
    return matchedCustomer?.full_name || matchedCustomer?.name || 'Unknown';
  };

  if (loading && orders.length === 0) {
    return (
      <Layout title="Orders">
        <Loading />
      </Layout>
    );
  }

  return (
    <Layout title="Orders">
      <div className="page-stack">
        {error && (
          <Alert
            type="error"
            message={error}
            onClose={() => setError(null)}
          />
        )}
        {success && (
          <Alert
            type="success"
            message={success}
            onClose={() => setSuccess(null)}
          />
        )}

        <div className="page-actions">
          <button
            className="btn btn-primary"
            onClick={() => setShowForm((current) => !current)}
          >
            {showForm ? 'Cancel' : '+ Create Order'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <div className="card-header">
              <h3>Create New Order</h3>
            </div>
            <form onSubmit={handleSubmit} className="form-container">
              <div className="form-group full-width">
                <label>Customer *</label>
                <select
                  value={formData.customer_id}
                  onChange={handleCustomerChange}
                  required
                >
                  <option value="">Select customer</option>
                  {customers.map((customer) => (
                    <option key={customer.id} value={customer.id}>
                      {customer.full_name || customer.name}
                    </option>
                  ))}
                </select>
                {formErrors.customer_id && (
                  <div className="field-error">{formErrors.customer_id}</div>
                )}
              </div>

              <div className="form-group full-width">
                <h4>Order Items</h4>
              </div>

              {orderItems.map((item, index) => (
                <div key={index} className="order-item-row">
                  <div>
                    <label>Product</label>
                    <select
                      value={item.product_id}
                      onChange={(e) =>
                        handleOrderItemChange(index, 'product_id', e.target.value)
                      }
                      required
                    >
                      <option value="">Select product</option>
                      {products.map((product) => (
                        <option key={product.id} value={product.id}>
                          {product.name} - ${parseFloat(product.price).toFixed(2)}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label>Quantity</label>
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) =>
                        handleOrderItemChange(index, 'quantity', e.target.value)
                      }
                      required
                    />
                  </div>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => removeOrderItem(index)}
                    disabled={orderItems.length === 1}
                  >
                    Remove
                  </button>
                </div>
              ))}

              <div className="form-group full-width">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={addOrderItem}
                >
                  + Add Item
                </button>
              </div>

              {formErrors.items && (
                <div className="inline-error">
                  {formErrors.items}
                </div>
              )}

              <div className="btn-group">
                <button type="submit" className="btn btn-success" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Order'}
                </button>
                <button type="button" className="btn btn-secondary" onClick={resetForm}>
                  Clear
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="card">
          <div className="card-header">
            <h3>All Orders ({orders.length})</h3>
          </div>
          {orders.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">O</div>
              <div className="empty-state-title">No Orders</div>
              <div className="empty-state-message">Start by creating your first order</div>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Customer</th>
                    <th>Items</th>
                    <th>Total Amount</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((order) => {
                    const itemCount = (order.items || order.order_items || order.products || []).length;
                    const status = order.status || 'Pending';
                    return (
                      <tr key={order.id}>
                        <td className="cell-strong">#{order.id}</td>
                        <td>{getOrderCustomerName(order)}</td>
                        <td>{itemCount}</td>
                        <td>${Number(order.total_amount || 0).toFixed(2)}</td>
                        <td>
                          <span className="pill pill-warning">{status}</span>
                        </td>
                        <td>
                          {order.created_at
                            ? new Date(order.created_at).toLocaleDateString()
                            : 'N/A'}
                        </td>
                        <td>
                          <div className="btn-group">
                            <button
                              className="btn btn-primary btn-compact"
                              onClick={() => navigate(`/orders/${order.id}`)}
                              disabled={loading}
                            >
                              View
                            </button>
                            <button
                              className="btn btn-danger btn-compact"
                              onClick={() => setConfirmDelete(order.id)}
                              disabled={loading}
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {confirmDelete && (
          <ConfirmDialog
            title="Delete Order"
            message="Are you sure you want to delete this order? This action cannot be undone."
            confirmText="Delete"
            cancelText="Cancel"
            isDangerous={true}
            onConfirm={() => handleDelete(confirmDelete)}
            onCancel={() => setConfirmDelete(null)}
          />
        )}
      </div>
    </Layout>
  );
}

export default Orders;
