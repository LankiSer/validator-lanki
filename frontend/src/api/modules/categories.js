import { api } from '../http/client'

export function fetchCategories() {
  return api.get('/categories')
}
