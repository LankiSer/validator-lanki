<template>
  <div class="toolbar card">
    <div v-if="canFilter" class="row">
      <div class="form-group grow">
        <label>Поиск</label>
        <input v-model="localSearch" class="input" placeholder="Артикул, название, описание..." />
      </div>
      <div class="form-group">
        <label>Производитель</label>
        <select v-model="localProducer" class="select">
          <option :value="null">Все производители</option>
          <option v-for="m in producers" :key="m.id" :value="m.id">{{ m.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Сортировка</label>
        <select v-model="localSort" class="select">
          <option value="">Без сортировки</option>
          <option value="amount_in_stock:asc">Количество ↑</option>
          <option value="amount_in_stock:desc">Количество ↓</option>
          <option value="price:asc">Цена ↑</option>
          <option value="price:desc">Цена ↓</option>
          <option value="discount:asc">Скидка ↑</option>
          <option value="discount:desc">Скидка ↓</option>
        </select>
      </div>
    </div>
    <p v-else class="muted">Гость и клиент видят список без поиска, сортировки и фильтрации.</p>
    <button v-if="isAdmin" class="btn btn-primary" @click="$emit('add')">Добавить товар</button>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { canFilterSortSearch, canManageProducts } from '../../../store/auth'

const props = defineProps({ producers: Array, modelValue: Object })
const emit = defineEmits(['update:modelValue', 'add'])

const canFilter = computed(() => canFilterSortSearch())
const isAdmin = computed(() => canManageProducts())

const localSearch = ref(props.modelValue.search || '')
const localProducer = ref(props.modelValue.producer_id ?? null)
const localSort = ref(
  props.modelValue.sort_by
    ? `${props.modelValue.sort_by}:${props.modelValue.sort_dir || 'asc'}`
    : ''
)

watch([localSearch, localProducer, localSort], () => {
  const [sortBy, sortDir] = localSort.value ? localSort.value.split(':') : [null, 'asc']
  emit('update:modelValue', {
    search: localSearch.value,
    producer_id: localProducer.value,
    sort_by: sortBy,
    sort_dir: sortDir,
  })
})
</script>

<style scoped>
.toolbar {
  display: grid;
  gap: 12px;
  margin-bottom: 16px;
}
.row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 12px;
}
.grow {
  margin-bottom: 0;
}
@media (max-width: 900px) {
  .row {
    grid-template-columns: 1fr;
  }
}
</style>
