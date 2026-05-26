<template>
  <form class="card grid" @submit.prevent="submit">
    <h3>{{ category ? 'Редактировать категорию' : 'Новая категория' }}</h3>
    <div class="form-group">
      <label>Название</label>
      <input v-model="name" class="input" required />
    </div>
    <button class="btn btn-primary" type="submit">Сохранить</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({ category: Object })
const emit = defineEmits(['save'])

const name = ref('')

watch(
  () => props.category,
  (value) => {
    name.value = value?.name || ''
  },
  { immediate: true }
)

function submit() {
  emit('save', name.value)
}
</script>
