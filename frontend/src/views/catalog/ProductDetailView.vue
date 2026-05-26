<template>
  <section v-if="product" class="card product-detail">
    <img :src="imageSrc" :alt="product.name" class="image" />
    <div>
      <h1>{{ product.name }}</h1>
      <p class="muted">{{ product.description }}</p>
      <p><strong>{{ product.price.toLocaleString('ru-RU') }} ₽</strong></p>
      <p>В наличии: {{ product.stock }} шт.</p>
      <router-link to="/" class="btn btn-secondary">Назад в каталог</router-link>
    </div>
  </section>
  <p v-else class="muted">Загрузка...</p>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchProduct } from '../../api/modules/products'

const route = useRoute()
const product = ref(null)

const imageSrc = computed(() => {
  return product.value?.image_url || 'https://placehold.co/600x400?text=No+Image'
})

onMounted(async () => {
  product.value = await fetchProduct(route.params.id)
})
</script>

<style scoped>
.product-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.image {
  width: 100%;
  border-radius: 12px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .product-detail {
    grid-template-columns: 1fr;
  }
}
</style>
