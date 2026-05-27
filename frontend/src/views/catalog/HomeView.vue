<template>
  <section>
    <h1 class="page-title">Каталог строительных материалов</h1>
    <ProductToolbar v-model="filters" :producers="producers" @add="openAdd" />
    <div v-if="loading" class="muted">Загрузка...</div>
    <div v-else class="list">
      <ProductRow v-for="item in products" :key="item.id" :product="item" @edit="openEdit" />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchProducers } from '../../api/modules/manufacturers'
import { fetchProducts } from '../../api/modules/products'
import ProductRow from '../../components/products/catalog/ProductRow.vue'
import ProductToolbar from '../../components/products/catalog/ProductToolbar.vue'
import { useDialog } from '../../composables/useDialog'
import { canManageProducts } from '../../store/auth'

const router = useRouter()
const { showError } = useDialog()

const products = ref([])
const producers = ref([])
const loading = ref(true)
const filters = ref({ search: '', producer_id: null, sort_by: null, sort_dir: 'asc' })

async function load() {
  loading.value = true
  try {
    products.value = await fetchProducts(filters.value)
  } catch (err) {
    showError(err.message)
  } finally {
    loading.value = false
  }
}

function openAdd() {
  if (sessionStorage.getItem('edit_lock')) {
    showError('Закройте текущее окно редактирования.')
    return
  }
  router.push('/products/new')
}

function openEdit(product) {
  if (!canManageProducts()) return
  if (sessionStorage.getItem('edit_lock')) {
    showError('Уже открыто окно редактирования.')
    return
  }
  router.push(`/products/${product.id}/edit`)
}

onMounted(async () => {
  producers.value = await fetchProducers()
  await load()
})

watch(filters, load, { deep: true })
</script>

<style scoped>
.list {
  display: grid;
  gap: 12px;
}
</style>
