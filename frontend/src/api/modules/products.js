import { api } from '../http/client'

export function fetchProducts(categoryId = null) {
  const query = categoryId ? `?category_id=${categoryId}` : ''
  return api.get(`/products${query}`)
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

export function uploadProductImage(id, file) {
  const formData = new FormData()
  formData.append('file', file)
  return api.upload(`/products/${id}/image`, formData)
}
