<template>
  <table class="table card">
    <thead>
      <tr>
        <th>ID</th>
        <th>Название</th>
        <th>Цена</th>
        <th>Остаток</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in products" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.price }} ₽</td>
        <td>{{ item.stock }}</td>
        <td class="actions">
          <button class="btn btn-secondary" @click="$emit('edit', item)">Изменить</button>
          <button class="btn btn-danger" @click="$emit('remove', item.id)">Удалить</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
defineProps({ products: Array })
defineEmits(['edit', 'remove'])
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid var(--border);
}

.actions {
  display: flex;
  gap: 8px;
}
</style>
