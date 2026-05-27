<template>
  <form class="card auth-form" @submit.prevent="handleSubmit">
    <h2>Вход в систему</h2>
    <div class="form-group">
      <label>Логин</label>
      <input v-model="form.login" class="input" required />
    </div>
    <div class="form-group">
      <label>Пароль</label>
      <input v-model="form.password" class="input" type="password" required />
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <button class="btn btn-primary" type="submit">Войти</button>
    <button class="btn btn-secondary guest-btn" type="button" @click="$emit('guest')">
      Войти как гость
    </button>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  onSubmit: { type: Function, required: true },
})

defineEmits(['guest'])

const form = reactive({ login: '', password: '' })
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    await props.onSubmit({ ...form })
  } catch (err) {
    error.value = err.message
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 420px;
  margin: 0 auto;
}
.guest-btn {
  width: 100%;
  margin-top: 8px;
}
</style>
