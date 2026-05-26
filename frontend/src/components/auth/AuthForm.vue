<template>
  <form class="card auth-form" @submit.prevent="handleSubmit">
    <h2>{{ title }}</h2>
    <div v-if="showEmail" class="form-group">
      <label>Email</label>
      <input v-model="form.email" class="input" type="email" required />
    </div>
    <div v-if="showUsername" class="form-group">
      <label>Имя пользователя</label>
      <input v-model="form.username" class="input" required />
    </div>
    <div class="form-group">
      <label>Пароль</label>
      <input v-model="form.password" class="input" type="password" required />
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <button class="btn btn-primary" type="submit">{{ buttonText }}</button>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  title: String,
  buttonText: String,
  showEmail: { type: Boolean, default: true },
  showUsername: { type: Boolean, default: false },
  onSubmit: { type: Function, required: true },
})

const form = reactive({ email: '', username: '', password: '' })
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
</style>
