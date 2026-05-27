import { api } from '../http/client'

export function fetchProducts(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      query.append(key, value)
    }
  })
  const suffix = query.toString() ? `?${query}` : ''
  return api.get(`/products${suffix}`)
}

export function fetchProduct(id) {
  return api.get(`/products/${id}`)
}

export function createProduct(payload) {
  return api.post('/products', payload)
}

export function updateProduct(id, payload) {
  return api.put(`/products/${id}`, payload)
}

export function deleteProduct(id) {
  return api.delete(`/products/${id}`)
}

export function uploadProductPhoto(id, file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.upload(`/products/${id}/photo`, formData)
}

export function fetchProviders() {
  return api.get('/products/references/providers')
}

export function fetchUnits() {
  return api.get('/products/references/units')
}

export function fetchPickUpPoints() {
  return api.get('/products/references/pick-up-points')
}
