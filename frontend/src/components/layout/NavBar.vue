<template>
  <header class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="logo">Mini Shop</router-link>
      <nav class="links">
        <router-link to="/">Каталог</router-link>
        <template v-if="user">
          <span class="user">{{ user.username }}</span>
          <button class="btn btn-secondary" @click="logout">Выйти</button>
        </template>
        <template v-else>
          <router-link to="/login">Вход</router-link>
          <router-link to="/register">Регистрация</router-link>
        </template>
        <template v-if="user?.is_admin">
          <router-link to="/admin/products">Товары</router-link>
          <router-link to="/admin/categories">Категории</router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuth, getUser } from '../../store/auth'

const router = useRouter()
const user = computed(() => getUser())

function logout() {
  clearAuth()
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
  font-size: 1.2rem;
}

.links {
  display: flex;
  gap: 14px;
  align-items: center;
}

.user {
  color: var(--muted);
}
</style>
