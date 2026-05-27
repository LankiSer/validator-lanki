<template>
  <header class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="logo">СтройМатериалы</router-link>
      <nav class="links">
        <router-link to="/">Товары</router-link>
        <router-link v-if="canViewOrders()" to="/orders">Заказы</router-link>
        <span v-if="user" class="user">{{ user.full_name }} ({{ roleLabel }})</span>
        <button v-if="user || !isGuest()" class="btn btn-secondary" @click="logout">Выйти</button>
        <router-link v-else to="/login">Вход</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  canViewOrders,
  clearAuth,
  getRole,
  getUser,
  isGuest,
  ROLES,
  setGuest,
} from '../../store/auth'

const router = useRouter()
const user = computed(() => getUser())
const roleLabel = computed(() => {
  const map = {
    [ROLES.ADMIN]: 'Администратор',
    [ROLES.MANAGER]: 'Менеджер',
    [ROLES.CLIENT]: 'Клиент',
    [ROLES.GUEST]: 'Гость',
  }
  return map[getRole()] || 'Гость'
})

function logout() {
  clearAuth()
  setGuest()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid var(--border);
}
.navbar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  padding-bottom: 14px;
}
.logo {
  font-weight: 800;
}
.links {
  display: flex;
  gap: 14px;
  align-items: center;
}
.user {
  color: var(--muted);
  font-size: 0.9rem;
}
</style>
