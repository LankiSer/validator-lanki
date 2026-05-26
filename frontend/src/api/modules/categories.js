import { api } from '../http/client'

export function fetchCategories() {
  return api.get('/categories')
}

export function createCategory(name) {
  return api.post('/categories', { name })
}

export function updateCategory(id, name) {
  return api.put(`/categories/${id}`, { name })
}

export function deleteCategory(id) {
  return api.delete(`/categories/${id}`)
}
