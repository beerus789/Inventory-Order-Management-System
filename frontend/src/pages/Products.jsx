import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Loading from '../components/Loading';
import Alert from '../components/Alert';
import ConfirmDialog from '../components/ConfirmDialog';
import { getProducts, createProduct, updateProduct, deleteProduct } from '../api/productApi';

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    price: '',
    quantity_in_stock: '',
  });
  const [formErrors, setFormErrors] = useState({
    name: '',
    sku: '',
    price: '',
    quantity_in_stock: '',
  });

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getProducts();
      setProducts(response.data?.data || response.data || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load products');
      console.error('Error loading products:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      sku: '',
      price: '',
      quantity_in_stock: '',
    });
    setFormErrors({
      name: '',
      sku: '',
      price: '',
      quantity_in_stock: '',
    });
    setEditingId(null);
    setShowForm(false);
  };

  const validateForm = () => {
    const errors = { name: '', sku: '', price: '', quantity_in_stock: '' };
    let isValid = true;

    if (!formData.name.trim()) {
      errors.name = 'Product name is required';
      isValid = false;
    }

    if (!formData.sku.trim()) {
      errors.sku = 'SKU is required';
      isValid = false;
    }

    if (!formData.price) {
      errors.price = 'Price is required';
      isValid = false;
    } else if (parseFloat(formData.price) < 0) {
      errors.price = 'Price cannot be negative';
      isValid = false;
    }

    if (formData.quantity_in_stock === '') {
      errors.quantity_in_stock = 'Quantity is required';
      isValid = false;
    } else if (parseInt(formData.quantity_in_stock) < 0) {
      errors.quantity_in_stock = 'Quantity cannot be negative';
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
        name: formData.name,
        sku: formData.sku,
        price: parseFloat(formData.price),
        quantity: parseInt(formData.quantity_in_stock),
      };

      if (editingId) {
        await updateProduct(editingId, payload);
        setSuccess('Product updated successfully');
      } else {
        await createProduct(payload);
        setSuccess('Product created successfully');
      }

      await loadProducts();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save product');
      console.error('Error saving product:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (product) => {
    setFormData({
      name: product.name,
      sku: product.sku || product.code || '',
      price: product.price,
      quantity_in_stock: product.quantity_in_stock || product.quantity || 0,
    });
    setFormErrors({
      name: '',
      sku: '',
      price: '',
      quantity_in_stock: '',
    });
    setEditingId(product.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    try {
      setLoading(true);
      await deleteProduct(id);
      setSuccess('Product deleted successfully');
      await loadProducts();
      setConfirmDelete(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete product');
      console.error('Error deleting product:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && products.length === 0) {
    return <Layout title="Products"><Loading /></Layout>;
  }

  return (
    <Layout title="Products">
      <div>
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

        <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
          <button
            className="btn btn-primary"
            onClick={() => {
              setEditingId(null);
              setFormData({ name: '', sku: '', price: '', quantity_in_stock: '' });
              setShowForm(!showForm);
            }}
          >
            {showForm ? '✕ Cancel' : '+ Add Product'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <div className="card-header">
              <h3>{editingId ? 'Edit Product' : 'Add New Product'}</h3>
            </div>
            <form onSubmit={handleSubmit} className="form-container">
              <div className="form-group">
                <label>Product Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  style={formErrors.name ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.name && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.name}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>SKU *</label>
                <input
                  type="text"
                  name="sku"
                  value={formData.sku}
                  onChange={handleInputChange}
                  required
                  style={formErrors.sku ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.sku && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.sku}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>Price *</label>
                <input
                  type="number"
                  name="price"
                  step="0.01"
                  min="0"
                  value={formData.price}
                  onChange={handleInputChange}
                  required
                  style={formErrors.price ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.price && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.price}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>Quantity in Stock *</label>
                <input
                  type="number"
                  name="quantity_in_stock"
                  min="0"
                  value={formData.quantity_in_stock}
                  onChange={handleInputChange}
                  required
                  style={formErrors.quantity_in_stock ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.quantity_in_stock && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.quantity_in_stock}
                  </div>
                )}
              </div>
              <div className="btn-group">
                <button type="submit" className="btn btn-success" disabled={loading}>
                  {loading ? 'Saving...' : editingId ? 'Update Product' : 'Create Product'}
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
            <h3>All Products ({products.length})</h3>
          </div>
          {products.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📦</div>
              <div className="empty-state-title">No Products</div>
              <div className="empty-state-message">Start by adding your first product</div>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>SKU</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((product) => {
                    const quantity = product.quantity_in_stock || product.quantity || 0;
                    const isLowStock = quantity <= 5;
                    return (
                      <tr key={product.id}>
                        <td>{product.name}</td>
                        <td>{product.sku || product.code || 'N/A'}</td>
                        <td>${parseFloat(product.price).toFixed(2)}</td>
                        <td>{quantity}</td>
                        <td>
                          {isLowStock ? (
                            <span style={{ color: '#e74c3c', fontWeight: 'bold' }}>
                              ⚠ Low Stock
                            </span>
                          ) : (
                            <span style={{ color: '#27ae60' }}>✓ In Stock</span>
                          )}
                        </td>
                        <td>
                          <div className="btn-group">
                            <button
                              className="btn btn-warning"
                              onClick={() => handleEdit(product)}
                              disabled={loading}
                            >
                              Edit
                            </button>
                            <button
                              className="btn btn-danger"
                              onClick={() => setConfirmDelete(product.id)}
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
            title="Delete Product"
            message="Are you sure you want to delete this product? This action cannot be undone."
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

export default Products;
