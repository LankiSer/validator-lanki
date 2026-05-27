<template>
  <article
    class="card order-row"
    :class="{ clickable: canEdit }"
    @click="canEdit ? $emit('edit', order) : null"
  >
    <div>
      <div><strong>Артикул:</strong> {{ order.article }}</div>
      <div><strong>Оформил:</strong> {{ order.user_full_name }} ({{ order.user_login }})</div>
      <div><strong>Статус:</strong> {{ order.status_name }}</div>
      <div><strong>Пункт выдачи:</strong> {{ order.pick_up_address }}</div>
      <div><strong>Код получения:</strong> {{ order.reception_code }}</div>
      <div><strong>Дата оформления:</strong> {{ order.creation_date }}</div>
    </div>
    <div class="delivery">
      <div><strong>Дата доставки</strong></div>
      <div>{{ order.delivery_date }}</div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { canManageOrders } from '../../store/auth'

defineProps({ order: Object })
defineEmits(['edit'])

const canEdit = computed(() => canManageOrders())
</script>

<style scoped>
.order-row {
  display: grid;
  grid-template-columns: 1fr 160px;
  gap: 16px;
}
.clickable {
  cursor: pointer;
}
.delivery {
  border-left: 3px solid var(--primary);
  padding-left: 12px;
}
</style>
