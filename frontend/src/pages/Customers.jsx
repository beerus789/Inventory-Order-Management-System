import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Loading from '../components/Loading';
import Alert from '../components/Alert';
import ConfirmDialog from '../components/ConfirmDialog';
import { getCustomers, createCustomer, deleteCustomer } from '../api/customerApi';

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
  });
  const [formErrors, setFormErrors] = useState({
    name: '',
    email: '',
    phone: '',
  });

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getCustomers();
      setCustomers(response.data?.data || response.data || []);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load customers');
      console.error('Error loading customers:', err);
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
      email: '',
      phone: '',
    });
    setFormErrors({
      name: '',
      email: '',
      phone: '',
    });
    setShowForm(false);
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePhone = (phone) => {
    // Remove all non-digit characters
    const digitsOnly = phone.replace(/\D/g, '');
    // Must be 10-20 digits
    return digitsOnly.length >= 10 && digitsOnly.length <= 20;
  };

  const validateForm = () => {
    const errors = { name: '', email: '', phone: '' };
    let isValid = true;

    // Name validation
    if (!formData.name.trim()) {
      errors.name = 'Customer name is required';
      isValid = false;
    }

    // Email validation
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
      isValid = false;
    } else if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address (e.g., user@example.com)';
      isValid = false;
    }

    // Phone validation
    if (!formData.phone.trim()) {
      errors.phone = 'Phone number is required';
      isValid = false;
    } else if (!validatePhone(formData.phone)) {
      errors.phone = 'Phone must be 10-20 digits (can include dashes, spaces, parentheses)';
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
        email: formData.email,
        phone: formData.phone,
      };

      await createCustomer(payload);
      setSuccess('Customer created successfully');
      await loadCustomers();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create customer');
      console.error('Error creating customer:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      setLoading(true);
      await deleteCustomer(id);
      setSuccess('Customer deleted successfully');
      await loadCustomers();
      setConfirmDelete(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete customer');
      console.error('Error deleting customer:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && customers.length === 0) {
    return <Layout title="Customers"><Loading /></Layout>;
  }

  return (
    <Layout title="Customers">
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

        <div style={{ marginBottom: '20px' }}>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? '✕ Cancel' : '+ Add Customer'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <div className="card-header">
              <h3>Add New Customer</h3>
            </div>
            <form onSubmit={handleSubmit} className="form-container">
              <div className="form-group">
                <label>Full Name *</label>
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
                <label>Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  style={formErrors.email ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.email && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.email}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>Phone Number *</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                  placeholder="e.g., 123-456-7890 or (123) 456-7890"
                  style={formErrors.phone ? { borderColor: '#dc3545' } : {}}
                />
                {formErrors.phone && (
                  <div style={{ color: '#dc3545', fontSize: '13px', marginTop: '5px' }}>
                    {formErrors.phone}
                  </div>
                )}
              </div>
              <div className="btn-group">
                <button type="submit" className="btn btn-success" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Customer'}
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
            <h3>All Customers ({customers.length})</h3>
          </div>
          {customers.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">👥</div>
              <div className="empty-state-title">No Customers</div>
              <div className="empty-state-message">Start by adding your first customer</div>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map((customer) => (
                    <tr key={customer.id}>
                      <td>{customer.full_name || customer.name}</td>
                      <td>{customer.email}</td>
                      <td>{customer.phone}</td>
                      <td>
                        <button
                          className="btn btn-danger"
                          onClick={() => setConfirmDelete(customer.id)}
                          disabled={loading}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {confirmDelete && (
          <ConfirmDialog
            title="Delete Customer"
            message="Are you sure you want to delete this customer? This action cannot be undone."
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

export default Customers;
