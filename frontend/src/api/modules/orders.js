import { api } from '../http/client'

export function fetchOrderStatuses() {
  return api.get('/orders/statuses')
}

export function fetchOrders() {
  return api.get('/orders')
}

export function fetchOrder(id) {
  return api.get(`/orders/${id}`)
}

export function createOrder(payload) {
  return api.post('/orders', payload)
}

export function updateOrder(id, payload) {
  return api.put(`/orders/${id}`, payload)
}

export function deleteOrder(id) {
  return api.delete(`/orders/${id}`)
}
