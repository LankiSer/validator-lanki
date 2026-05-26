<template>
  <ul class="card list">
    <li v-for="item in categories" :key="item.id">
      <span>{{ item.name }}</span>
      <div class="actions">
        <button class="btn btn-secondary" @click="$emit('edit', item)">Изменить</button>
        <button class="btn btn-danger" @click="$emit('remove', item.id)">Удалить</button>
      </div>
    </li>
  </ul>
</template>

<script setup>
defineProps({ categories: Array })
defineEmits(['edit', 'remove'])
</script>

<style scoped>
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.actions {
  display: flex;
  gap: 8px;
}
</style>
