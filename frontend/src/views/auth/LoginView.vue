<template>
  <AuthForm :on-submit="handleLogin" @guest="enterGuest" />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { login } from '../../api/modules/auth'
import AuthForm from '../../components/auth/AuthForm.vue'
import { setGuest } from '../../store/auth'

const router = useRouter()

async function handleLogin(payload) {
  await login(payload)
  router.push('/')
}

function enterGuest() {
  setGuest()
  router.push('/')
}
</script>
