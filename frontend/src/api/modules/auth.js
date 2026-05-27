import { api } from '../http/client'
import { setAuth } from '../../store/auth'

export function login(payload) {
  return api.post('/auth/login', payload).then((data) => {
    setAuth(data.access_token, data.user)
    return data
  })
}

export function fetchProfile() {
  return api.get('/auth/me')
}
