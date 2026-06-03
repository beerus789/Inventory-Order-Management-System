import apiClient from './axios';

// Order API endpoints
export const getOrders = () => {
  return apiClient.get('/orders').then((res) => {
    const payload = res.data && (res.data.items || res.data.data)
      ? (res.data.items || res.data.data)
      : res.data;
    return { ...res, data: payload };
  });
};

export const getOrderById = (id) => {
  return apiClient.get(`/orders/${id}`);
};

export const createOrder = (data) => {
  return apiClient.post('/orders', data);
};

export const deleteOrder = (id) => {
  return apiClient.delete(`/orders/${id}`);
};
