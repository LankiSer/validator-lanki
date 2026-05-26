<template>
  <div class="filters card">
    <label>Категория</label>
    <select class="select" :value="modelValue" @change="onChange">
      <option :value="null">Все категории</option>
      <option v-for="cat in categories" :key="cat.id" :value="cat.id">
        {{ cat.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  categories: Array,
  modelValue: [Number, null],
})

const emit = defineEmits(['update:modelValue'])

function onChange(event) {
  const value = event.target.value
  emit('update:modelValue', value ? Number(value) : null)
}
</script>

<style scoped>
.filters {
  margin-bottom: 16px;
  display: grid;
  gap: 8px;
}
</style>
