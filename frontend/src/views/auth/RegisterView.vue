<template>
  <AuthForm
    title="Регистрация"
    button-text="Создать аккаунт"
    :show-username="true"
    :on-submit="handleRegister"
  />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { register } from '../../api/modules/auth'
import AuthForm from '../../components/auth/AuthForm.vue'

const router = useRouter()

async function handleRegister(payload) {
  await register(payload)
  router.push('/')
}
</script>
