import apiClient from './axios';

// Product API endpoints
export const getProducts = () => {
  return apiClient.get('/products').then((res) => {
    const payload = res.data && (res.data.items || res.data.data)
      ? (res.data.items || res.data.data)
      : res.data;
    return { ...res, data: payload };
  });
};

export const getProductById = (id) => {
  return apiClient.get(`/products/${id}`);
};

export const createProduct = (data) => {
  return apiClient.post('/products', data);
};

export const updateProduct = (id, data) => {
  return apiClient.put(`/products/${id}`, data);
};

export const deleteProduct = (id) => {
  return apiClient.delete(`/products/${id}`);
};
