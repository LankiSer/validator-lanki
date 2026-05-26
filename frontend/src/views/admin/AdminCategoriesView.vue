<template>
  <section class="grid">
    <h1 class="page-title">Управление категориями</h1>
    <CategoryForm :category="selected" @save="saveCategory" />
    <CategoryList :categories="categories" @edit="editCategory" @remove="removeCategory" />
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  createCategory,
  deleteCategory,
  fetchCategories,
  updateCategory,
} from '../../api/modules/categories'
import CategoryForm from '../../components/categories/CategoryForm.vue'
import CategoryList from '../../components/categories/CategoryList.vue'

const categories = ref([])
const selected = ref(null)

async function reload() {
  categories.value = await fetchCategories()
}

onMounted(reload)

function editCategory(item) {
  selected.value = { ...item }
}

async function saveCategory(name) {
  if (selected.value?.id) {
    await updateCategory(selected.value.id, name)
  } else {
    await createCategory(name)
  }
  selected.value = null
  await reload()
}

async function removeCategory(id) {
  if (confirm('Удалить категорию?')) {
    await deleteCategory(id)
    await reload()
  }
}
</script>

<style scoped>
.grid {
  gap: 20px;
}
</style>
