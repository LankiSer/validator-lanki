<template>
  <section class="card edit-page">
    <div class="head">
      <h1 class="page-title">{{ isNew ? 'Добавление заказа' : 'Редактирование заказа' }}</h1>
      <button class="btn btn-secondary" @click="goBack">Назад</button>
    </div>
    <form class="grid-form" @submit.prevent="save">
      <div v-if="!isNew" class="form-group">
        <label>ID</label>
        <input class="input" :value="orderId" readonly />
      </div>
      <div v-if="!isNew && orderUser" class="form-group">
        <label>Оформил заказ</label>
        <input class="input" :value="`${orderUser.full_name} (${orderUser.login})`" readonly />
      </div>
      <p v-else-if="isNew" class="muted">Заказ будет привязан к текущему пользователю.</p>
      <div class="form-group">
        <label>Артикул заказа</label>
        <input v-model="form.article" class="input" maxlength="10" required />
      </div>
      <div class="form-group">
        <label>Статус заказа</label>
        <select v-model.number="form.status_id" class="select" required>
          <option v-for="s in statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Пункт выдачи</label>
        <select v-model.number="form.pick_up_point_id" class="select" required>
          <option v-for="p in pickUpPoints" :key="p.id" :value="p.id">{{ p.full_address }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>Код получения</label>
        <input v-model.number="form.reception_code" class="input" type="number" required />
      </div>
      <div class="form-group">
        <label>Дата оформления</label>
        <input v-model="form.creation_date" class="input" type="date" required />
      </div>
      <div class="form-group">
        <label>Дата доставки</label>
        <input v-model="form.delivery_date" class="input" type="date" required />
      </div>

      <div v-if="isNew" class="lines-block">
        <label>Позиции заказа</label>
        <div v-for="(line, index) in lines" :key="index" class="line-row">
          <input
            v-model.number="line.product_id"
            class="input"
            type="number"
            min="1"
            placeholder="ID товара"
            required
          />
          <input
            v-model.number="line.amount"
            class="input"
            type="number"
            min="1"
            placeholder="Кол-во"
            required
          />
          <button class="btn btn-secondary" type="button" @click="removeLine(index)">×</button>
        </div>
        <button class="btn btn-secondary" type="button" @click="addLine">Добавить позицию</button>
      </div>
      <div v-else-if="savedLines.length" class="lines-readonly">
        <label>Позиции заказа</label>
        <ul>
          <li v-for="line in savedLines" :key="line.product_id">
            Товар #{{ line.product_id }} — {{ line.amount }} шт.
          </li>
        </ul>
      </div>

      <div class="actions">
        <button class="btn btn-primary" type="submit">Сохранить</button>
        <button v-if="!isNew" class="btn btn-danger" type="button" @click="remove">Удалить</button>
      </div>
    </form>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  createOrder,
  deleteOrder,
  fetchOrder,
  fetchOrderStatuses,
  updateOrder,
} from '../../api/modules/orders'
import { fetchPickUpPoints } from '../../api/modules/products'
import { useDialog } from '../../composables/useDialog'

const route = useRoute()
const router = useRouter()
const { showError, showInfo, confirmAction } = useDialog()

const isNew = computed(() => route.name === 'order-new')
const orderId = computed(() => Number(route.params.id))
const statuses = ref([])
const pickUpPoints = ref([])
const orderUser = ref(null)
const savedLines = ref([])
const lines = ref([{ product_id: null, amount: 1 }])

const form = reactive({
  article: '',
  status_id: null,
  pick_up_point_id: null,
  reception_code: 0,
  creation_date: '',
  delivery_date: '',
})

function addLine() {
  lines.value.push({ product_id: null, amount: 1 })
}

function removeLine(index) {
  if (lines.value.length > 1) {
    lines.value.splice(index, 1)
  }
}

onMounted(async () => {
  statuses.value = await fetchOrderStatuses()
  pickUpPoints.value = await fetchPickUpPoints()
  if (!isNew.value) {
    const order = await fetchOrder(orderId.value)
    orderUser.value = {
      login: order.user_login,
      full_name: order.user_full_name,
    }
    Object.assign(form, {
      article: order.article,
      status_id: order.status_id,
      pick_up_point_id: order.pick_up_point_id,
      reception_code: order.reception_code,
      creation_date: order.creation_date,
      delivery_date: order.delivery_date,
    })
    savedLines.value = order.lines || []
  } else {
    form.status_id = statuses.value[0]?.id
    form.pick_up_point_id = pickUpPoints.value[0]?.id
    const today = new Date().toISOString().slice(0, 10)
    form.creation_date = today
    form.delivery_date = today
    form.reception_code = Math.floor(100000 + Math.random() * 900000)
  }
})

async function save() {
  try {
    if (isNew.value) {
      const payload = {
        ...form,
        lines: lines.value
          .filter((l) => l.product_id > 0)
          .map((l) => ({ product_id: l.product_id, amount: l.amount })),
      }
      await createOrder(payload)
    } else {
      await updateOrder(orderId.value, { ...form })
    }
    showInfo('Заказ сохранён.')
    router.push('/orders')
  } catch (err) {
    showError(err.message)
  }
}

async function remove() {
  if (!confirmAction('Удалить заказ?')) return
  try {
    await deleteOrder(orderId.value)
    showInfo('Заказ удалён.')
    router.push('/orders')
  } catch (err) {
    showError(err.message)
  }
}

function goBack() {
  router.push('/orders')
}
</script>

<style scoped>
.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.grid-form {
  margin-top: 16px;
}
.actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}
.line-row {
  display: grid;
  grid-template-columns: 1fr 120px 40px;
  gap: 8px;
  margin-bottom: 8px;
}
.lines-block,
.lines-readonly {
  margin-top: 12px;
}
.lines-readonly ul {
  margin: 8px 0 0;
  padding-left: 20px;
}
</style>
