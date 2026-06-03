import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import Loading from '../components/Loading';
import Alert from '../components/Alert';
import ConfirmDialog from '../components/ConfirmDialog';
import { getOrderById, deleteOrder } from '../api/orderApi';
import { getCustomerById } from '../api/customerApi';

function OrderDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [customerDetails, setCustomerDetails] = useState(null);

  useEffect(() => {
    loadOrderDetails();
  }, [id]);

  const loadOrderDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getOrderById(id);
      const loadedOrder = response.data?.data || response.data;
      setOrder(loadedOrder);

      if (!loadedOrder.customer && loadedOrder.customer_id) {
        try {
          const customerResponse = await getCustomerById(loadedOrder.customer_id);
          setCustomerDetails(customerResponse.data?.data || customerResponse.data);
        } catch (customerErr) {
          console.error('Error loading customer details:', customerErr);
          setCustomerDetails(null);
        }
      } else {
        setCustomerDetails(null);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load order details');
      console.error('Error loading order details:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      setLoading(true);
      await deleteOrder(id);
      setSuccess('Order deleted successfully');
      setTimeout(() => navigate('/orders'), 1500);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete order');
      console.error('Error deleting order:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout title="Order Details">
        <Loading />
      </Layout>
    );
  }

  if (!order) {
    return (
      <Layout title="Order Details">
        <Alert
          type="error"
          message="Order not found"
          onClose={() => navigate('/orders')}
        />
      </Layout>
    );
  }

  const orderItems = order.items || order.order_items || order.products || [];
  const customer = order.customer || customerDetails || {};

  return (
    <Layout title="Order Details">
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
          <button className="btn btn-secondary" onClick={() => navigate('/orders')}>
            Back to Orders
          </button>
        </div>

        <div className="card">
          <div className="card-header">
            <div>
              <h3>Order #{order.id}</h3>
              <p>{order.status || 'Pending'}</p>
            </div>
            <button
              className="btn btn-danger"
              onClick={() => setConfirmDelete(true)}
              disabled={loading}
            >
              Delete Order
            </button>
          </div>

          <div className="detail-grid">
            <div className="detail-block">
              <h4>Order Information</h4>
              <p><strong>Order ID:</strong> #{order.id}</p>
              <p><strong>Status:</strong> {order.status || 'Pending'}</p>
              <p>
                <strong>Created Date:</strong>{' '}
                {order.created_at ? new Date(order.created_at).toLocaleString() : 'N/A'}
              </p>
              <p><strong>Total Amount:</strong> ${Number(order.total_amount || 0).toFixed(2)}</p>
            </div>

            <div className="detail-block">
              <h4>Customer Information</h4>
              <p><strong>Name:</strong> {customer.full_name || customer.name || 'Unknown'}</p>
              <p><strong>Email:</strong> {customer.email || 'N/A'}</p>
              <p><strong>Phone:</strong> {customer.phone || 'N/A'}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3>Order Items</h3>
          </div>
          {orderItems.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">I</div>
              <div className="empty-state-title">No Items</div>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Product Name</th>
                    <th>SKU</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {orderItems.map((item, index) => {
                    const product = item.product || {};
                    const price = parseFloat(item.price || product.price || 0);
                    const quantity = item.quantity || 0;
                    const total = price * quantity;

                    return (
                      <tr key={index}>
                        <td className="cell-strong">{product.name || 'Unknown'}</td>
                        <td>{product.sku || product.code || 'N/A'}</td>
                        <td>{quantity}</td>
                        <td>${price.toFixed(2)}</td>
                        <td>${total.toFixed(2)}</td>
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
            onConfirm={handleDelete}
            onCancel={() => setConfirmDelete(false)}
          />
        )}
      </div>
    </Layout>
  );
}

export default OrderDetails;
