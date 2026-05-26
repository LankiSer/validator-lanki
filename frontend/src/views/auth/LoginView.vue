<template>
  <AuthForm
    title="Вход"
    button-text="Войти"
    :show-username="false"
    :on-submit="handleLogin"
  />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { login } from '../../api/modules/auth'
import AuthForm from '../../components/auth/AuthForm.vue'

const router = useRouter()

async function handleLogin(payload) {
  await login(payload)
  router.push('/')
}
</script>
