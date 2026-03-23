const API_BASE = '/api'

function getToken() {
  return localStorage.getItem('token')
}

export async function request(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  if (res.status === 204) return null
  return res.json()
}

// Auth
export const auth = {
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request('/auth/me'),
}

// Products
export const products = {
  list: (params = '') => request(`/products${params}`),
  all: () => request('/products/all'),
  get: (id) => request(`/products/${id}`),
  create: (data) => request('/products', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id) => request(`/products/${id}`, { method: 'DELETE' }),
}

// Predictions
export const predictions = {
  demand: () => request('/predict-demand'),
}

// Sales
export const sales = {
  list: (params = '') => request(`/sales${params}`),
  create: (data) => request('/sales', { method: 'POST', body: JSON.stringify(data) }),
  daily: (date) => request(`/sales/daily/${date}`),
}
