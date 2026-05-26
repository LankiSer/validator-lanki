<template>
  <form class="card grid" @submit.prevent="submit">
    <h3>{{ product ? 'Редактировать товар' : 'Новый товар' }}</h3>
    <div class="form-group">
      <label>Название</label>
      <input v-model="form.name" class="input" required />
    </div>
    <div class="form-group">
      <label>Описание</label>
      <textarea v-model="form.description" class="textarea" />
    </div>
    <div class="form-group">
      <label>Цена</label>
      <input v-model.number="form.price" class="input" type="number" min="1" step="0.01" required />
    </div>
    <div class="form-group">
      <label>Остаток</label>
      <input v-model.number="form.stock" class="input" type="number" min="0" required />
    </div>
    <div class="form-group">
      <label>Категория</label>
      <select v-model.number="form.category_id" class="select" required>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
    </div>
    <div class="form-group">
      <label>Фото</label>
      <input type="file" accept="image/*" @change="onFileChange" />
    </div>
    <button class="btn btn-primary" type="submit">Сохранить</button>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  product: Object,
  categories: Array,
})

const emit = defineEmits(['save'])

const form = reactive({
  name: '',
  description: '',
  price: 0,
  stock: 0,
  category_id: null,
})

let selectedFile = null

watch(
  () => props.product,
  (value) => {
    form.name = value?.name || ''
    form.description = value?.description || ''
    form.price = value?.price || 0
    form.stock = value?.stock || 0
    form.category_id = value?.category_id || props.categories[0]?.id || null
  },
  { immediate: true }
)

function onFileChange(event) {
  selectedFile = event.target.files[0] || null
}

function submit() {
  emit('save', { ...form, file: selectedFile })
  selectedFile = null
}
</script>
