<template>
  <section class="card edit-page">
    <div class="head">
      <h1 class="page-title">{{ isNew ? 'Добавление товара' : 'Редактирование товара' }}</h1>
      <button class="btn btn-secondary" @click="goBack">Назад</button>
    </div>

    <form class="grid" @submit.prevent="save">
      <img :src="imageSrc" alt="Фото товара" class="photo" />
      <div class="fields">
        <div v-if="!isNew" class="form-group">
          <label>ID</label>
          <input class="input" :value="productId" readonly />
        </div>
        <div class="form-group">
          <label>Артикул</label>
          <input v-model="form.article" class="input" maxlength="10" required />
        </div>
        <div class="form-group">
          <label>Наименование</label>
          <input v-model="form.name" class="input" maxlength="50" required />
        </div>
        <div class="form-group">
          <label>Категория</label>
          <select v-model.number="form.category_id" class="select" required>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="form.description" class="textarea" />
        </div>
        <div class="form-group">
          <label>Производитель</label>
          <select v-model.number="form.producer_id" class="select" required>
            <option v-for="m in producers" :key="m.id" :value="m.id">{{ m.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Поставщик</label>
          <select v-model.number="form.provider_id" class="select" required>
            <option v-for="s in providers" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Цена</label>
          <input v-model.number="form.price" class="input" type="number" min="0" step="0.01" required />
        </div>
        <div class="form-group">
          <label>Единица измерения</label>
          <select v-model.number="form.unit_id" class="select" required>
            <option v-for="u in units" :key="u.id" :value="u.id">{{ u.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Количество на складе</label>
          <input v-model.number="form.amount_in_stock" class="input" type="number" min="0" step="0.01" required />
        </div>
        <div class="form-group">
          <label>Текущая скидка (%)</label>
          <input v-model.number="form.discount" class="input" type="number" min="0" max="100" step="0.01" />
        </div>
        <div class="form-group">
          <label>Фото (до 300×200)</label>
          <input type="file" accept="image/*" @change="onFile" />
        </div>
        <div class="actions">
          <button class="btn btn-primary" type="submit">Сохранить</button>
          <button v-if="!isNew" class="btn btn-danger" type="button" @click="remove">Удалить</button>
        </div>
      </div>
    </form>
  </section>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCategories } from '../../api/modules/categories'
import { fetchProducers } from '../../api/modules/manufacturers'
import {
  createProduct,
  deleteProduct,
  fetchProduct,
  fetchProviders,
  fetchUnits,
  updateProduct,
  uploadProductPhoto,
} from '../../api/modules/products'
import { useDialog } from '../../composables/useDialog'

const route = useRoute()
const router = useRouter()
const { showError, showInfo, confirmAction } = useDialog()

const isNew = computed(() => route.name === 'product-new')
const productId = computed(() => (isNew.value ? null : Number(route.params.id)))

const categories = ref([])
const producers = ref([])
const providers = ref([])
const units = ref([])
const imageUrl = ref(null)
let selectedFile = null

const form = reactive({
  article: '',
  name: '',
  description: '',
  category_id: null,
  producer_id: null,
  provider_id: null,
  unit_id: null,
  price: 0,
  amount_in_stock: 0,
  discount: 0,
})

const imageSrc = computed(() => imageUrl.value || '/picture.png')

onMounted(async () => {
  sessionStorage.setItem('edit_lock', route.fullPath)
  categories.value = await fetchCategories()
  producers.value = await fetchProducers()
  providers.value = await fetchProviders()
  units.value = await fetchUnits()
  if (!isNew.value) {
    const product = await fetchProduct(productId.value)
    Object.assign(form, {
      article: product.article,
      name: product.name,
      description: product.description,
      category_id: product.category_id,
      producer_id: product.producer_id,
      provider_id: product.provider_id,
      unit_id: product.unit_id,
      price: product.price,
      amount_in_stock: product.amount_in_stock,
      discount: product.discount,
    })
    imageUrl.value = product.photo
  } else {
    form.category_id = categories.value[0]?.id
    form.producer_id = producers.value[0]?.id
    form.provider_id = providers.value[0]?.id
    form.unit_id = units.value[0]?.id
  }
})

onUnmounted(() => sessionStorage.removeItem('edit_lock'))

function onFile(event) {
  selectedFile = event.target.files[0] || null
}

async function save() {
  if (form.price < 0 || form.amount_in_stock < 0) {
    showError('Цена и количество не могут быть отрицательными.')
    return
  }
  try {
    const payload = { ...form }
    let saved
    if (isNew.value) {
      saved = await createProduct(payload)
    } else {
      saved = await updateProduct(productId.value, payload)
    }
    if (selectedFile) {
      saved = await uploadProductPhoto(saved.id, selectedFile)
    }
    showInfo('Данные товара сохранены.')
    router.push('/')
  } catch (err) {
    showError(err.message)
  }
}

async function remove() {
  if (!confirmAction('Удалить товар? Это действие необратимо.')) return
  try {
    await deleteProduct(productId.value)
    showInfo('Товар удалён.')
    router.push('/')
  } catch (err) {
    showError(err.message)
  }
}

function goBack() {
  router.push('/')
}
</script>

<style scoped>
.edit-page {
  padding: 20px;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
  margin-top: 16px;
}
.photo {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid var(--border);
}
.actions {
  display: flex;
  gap: 10px;
}
@media (max-width: 800px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
