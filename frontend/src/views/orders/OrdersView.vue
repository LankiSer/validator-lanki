<template>
  <section>
    <div class="head">
      <h1 class="page-title">Список заказов</h1>
      <div class="actions">
        <button class="btn btn-secondary" @click="$router.push('/')">Назад</button>
        <button v-if="canEdit" class="btn btn-primary" @click="openAdd">Добавить заказ</button>
      </div>
    </div>
    <div v-if="loading" class="muted">Загрузка...</div>
    <div v-else class="list">
      <OrderRow v-for="item in orders" :key="item.id" :order="item" @edit="openEdit" />
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { fetchOrders } from '../../api/modules/orders'
import OrderRow from '../../components/orders/OrderRow.vue'
import { canManageOrders } from '../../store/auth'

const router = useRouter()
const orders = ref([])
const loading = ref(true)
const canEdit = canManageOrders()

async function reload() {
  loading.value = true
  orders.value = await fetchOrders()
  loading.value = false
}

function openAdd() {
  router.push('/orders/new')
}

function openEdit(order) {
  router.push(`/orders/${order.id}/edit`)
}

onMounted(reload)
</script>

<style scoped>
.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.actions {
  display: flex;
  gap: 8px;
}
.list {
  display: grid;
  gap: 12px;
}
</style>
