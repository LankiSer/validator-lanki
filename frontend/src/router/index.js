import { createRouter, createWebHistory } from 'vue-router'
import { isAdmin, isAuthenticated } from '../store/auth'
import HomeView from '../views/catalog/HomeView.vue'
import ProductDetailView from '../views/catalog/ProductDetailView.vue'
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import AdminProductsView from '../views/admin/AdminProductsView.vue'
import AdminCategoriesView from '../views/admin/AdminCategoriesView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/products/:id', name: 'product', component: ProductDetailView },
    {
      path: '/admin/products',
      name: 'admin-products',
      component: AdminProductsView,
      meta: { requiresAdmin: true },
    },
    {
      path: '/admin/categories',
      name: 'admin-categories',
      component: AdminCategoriesView,
      meta: { requiresAdmin: true },
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAdmin) {
    if (!isAuthenticated()) {
      return { name: 'login' }
    }
    if (!isAdmin()) {
      return { name: 'home' }
    }
  }
})

export default router
