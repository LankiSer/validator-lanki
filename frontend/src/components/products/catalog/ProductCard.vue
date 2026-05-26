<template>
  <article class="card product-card">
    <router-link :to="`/products/${product.id}`">
      <img :src="imageSrc" :alt="product.name" class="image" />
      <h3>{{ product.name }}</h3>
      <p class="muted">{{ product.description }}</p>
      <strong>{{ product.price.toLocaleString('ru-RU') }} ₽</strong>
    </router-link>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ product: Object })

const imageSrc = computed(() => {
  return props.product.image_url || 'https://placehold.co/400x260?text=No+Image'
})
</script>

<style scoped>
.product-card {
  overflow: hidden;
}

.image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

h3 {
  margin: 0 0 8px;
}
</style>
