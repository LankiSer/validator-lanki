import { api } from '../http/client'

export function fetchProducers() {
  return api.get('/producers')
}
