<template>
  <section>
    <h1 class="page-title">Каталог товаров</h1>
    <CategoryFilter v-model="categoryId" :categories="categories" />
    <div v-if="loading" class="muted">Загрузка...</div>
    <div v-else class="products-grid">
      <ProductCard v-for="item in products" :key="item.id" :product="item" />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { fetchCategories } from '../../api/modules/categories'
import { fetchProducts } from '../../api/modules/products'
import CategoryFilter from '../../components/products/catalog/CategoryFilter.vue'
import ProductCard from '../../components/products/catalog/ProductCard.vue'

const categories = ref([])
const products = ref([])
const categoryId = ref(null)
const loading = ref(true)

async function loadProducts() {
  loading.value = true
  products.value = await fetchProducts(categoryId.value)
  loading.value = false
}

onMounted(async () => {
  categories.value = await fetchCategories()
  await loadProducts()
})

watch(categoryId, loadProducts)
</script>
