<template>
  <section class="grid">
    <h1 class="page-title">Управление товарами</h1>
    <ProductForm :product="selected" :categories="categories" @save="saveProduct" />
    <ProductTable :products="products" @edit="editProduct" @remove="removeProduct" />
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchCategories } from '../../api/modules/categories'
import {
  createProduct,
  deleteProduct,
  fetchProducts,
  updateProduct,
  uploadProductImage,
} from '../../api/modules/products'
import ProductForm from '../../components/products/admin/ProductForm.vue'
import ProductTable from '../../components/products/admin/ProductTable.vue'

const products = ref([])
const categories = ref([])
const selected = ref(null)

async function reload() {
  products.value = await fetchProducts()
}

onMounted(async () => {
  categories.value = await fetchCategories()
  await reload()
})

function editProduct(item) {
  selected.value = { ...item }
}

async function saveProduct(payload) {
  const { file, ...data } = payload
  let saved

  if (selected.value?.id) {
    saved = await updateProduct(selected.value.id, data)
  } else {
    saved = await createProduct(data)
  }

  if (file) {
    saved = await uploadProductImage(saved.id, file)
  }

  selected.value = null
  await reload()
}

async function removeProduct(id) {
  if (confirm('Удалить товар?')) {
    await deleteProduct(id)
    await reload()
  }
}
</script>

<style scoped>
.grid {
  gap: 20px;
}
</style>
