const TOKEN_KEY = 'shop_token'
const USER_KEY = 'shop_user'
const ROLE_KEY = 'shop_role'

export const ROLES = {
  GUEST: 'guest',
  CLIENT: 'client',
  MANAGER: 'manager',
  ADMIN: 'admin',
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getUser() {
  const raw = localStorage.getItem(USER_KEY)
  return raw ? JSON.parse(raw) : null
}

export function getRole() {
  return localStorage.getItem(ROLE_KEY) || ROLES.GUEST
}

export function setAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
  localStorage.setItem(ROLE_KEY, user.role)
}

export function setGuest() {
  clearAuth()
  localStorage.setItem(ROLE_KEY, ROLES.GUEST)
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  localStorage.removeItem(ROLE_KEY)
}

export function isAuthenticated() {
  return Boolean(getToken())
}

export function isGuest() {
  return getRole() === ROLES.GUEST
}

export function isAdmin() {
  return getRole() === ROLES.ADMIN
}

export function isManager() {
  return getRole() === ROLES.MANAGER
}

export function canFilterSortSearch() {
  return getRole() === ROLES.MANAGER || getRole() === ROLES.ADMIN
}

export function canManageProducts() {
  return getRole() === ROLES.ADMIN
}

export function canViewOrders() {
  return getRole() === ROLES.MANAGER || getRole() === ROLES.ADMIN
}

export function canManageOrders() {
  return getRole() === ROLES.ADMIN
}
