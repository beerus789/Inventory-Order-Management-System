import apiClient from './axios';

// Customer API endpoints
export const getCustomers = () => {
  return apiClient.get('/customers').then((res) => {
    const payload = res.data && (res.data.items || res.data.data)
      ? (res.data.items || res.data.data)
      : res.data;
    return { ...res, data: payload };
  });
};

export const getCustomerById = (id) => {
  return apiClient.get(`/customers/${id}`);
};

export const createCustomer = (data) => {
  return apiClient.post('/customers', data);
};

export const deleteCustomer = (id) => {
  return apiClient.delete(`/customers/${id}`);
};
