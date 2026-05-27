<template>
  <article
    class="card product-row"
    :class="{ clickable: isAdmin }"
    @click="isAdmin ? $emit('edit', product) : null"
  >
    <img :src="imageSrc" :alt="product.name" class="thumb" />
    <div class="info">
      <h3>{{ product.article }} — {{ product.name }}</h3>
      <p class="muted">{{ product.description }}</p>
      <div class="meta">
        <span>Категория: {{ product.category_name }}</span>
        <span>Производитель: {{ product.producer_name }}</span>
        <span>Поставщик: {{ product.provider_name }}</span>
      </div>
    </div>
    <div class="price-block">
      <div><strong>{{ formatPrice(product.price) }} ₽</strong> / {{ product.unit_name }}</div>
      <div>На складе: {{ product.amount_in_stock }}</div>
      <div>Скидка: {{ product.discount }}%</div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { canManageProducts } from '../../../store/auth'

const props = defineProps({ product: Object })
defineEmits(['edit'])

const isAdmin = computed(() => canManageProducts())
const imageSrc = computed(() => props.product.photo || '/picture.png')

function formatPrice(value) {
  return Number(value).toLocaleString('ru-RU', { minimumFractionDigits: 2 })
}
</script>

<style scoped>
.product-row {
  display: grid;
  grid-template-columns: 120px 1fr 180px;
  gap: 16px;
  align-items: start;
}
.clickable {
  cursor: pointer;
}
.clickable:hover {
  border-color: var(--primary);
}
.thumb {
  width: 120px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}
.meta {
  display: grid;
  gap: 4px;
  font-size: 0.9rem;
  color: var(--muted);
}
.price-block {
  display: grid;
  gap: 4px;
  font-size: 0.9rem;
}
h3 {
  margin: 0 0 6px;
}
</style>
