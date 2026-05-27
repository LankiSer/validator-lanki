import { createRouter, createWebHistory } from 'vue-router'
import {
  canManageOrders,
  canManageProducts,
  canViewOrders,
  isAuthenticated,
} from '../store/auth'
import HomeView from '../views/catalog/HomeView.vue'
import ProductEditView from '../views/catalog/ProductEditView.vue'
import LoginView from '../views/auth/LoginView.vue'
import OrdersView from '../views/orders/OrdersView.vue'
import OrderEditView from '../views/orders/OrderEditView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: 'Каталог товаров' } },
    { path: '/login', name: 'login', component: LoginView, meta: { title: 'Вход' } },
    {
      path: '/products/new',
      name: 'product-new',
      component: ProductEditView,
      meta: { title: 'Добавление товара', requiresAdmin: true },
    },
    {
      path: '/products/:id/edit',
      name: 'product-edit',
      component: ProductEditView,
      meta: { title: 'Редактирование товара', requiresAdmin: true },
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersView,
      meta: { title: 'Заказы', requiresOrders: true },
    },
    {
      path: '/orders/new',
      name: 'order-new',
      component: OrderEditView,
      meta: { title: 'Добавление заказа', requiresAdmin: true },
    },
    {
      path: '/orders/:id/edit',
      name: 'order-edit',
      component: OrderEditView,
      meta: { title: 'Редактирование заказа', requiresAdmin: true },
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAdmin && !canManageProducts()) {
    return { name: 'home' }
  }
  if (to.meta.requiresOrders && !canViewOrders()) {
    return { name: 'home' }
  }
  if ((to.name === 'order-new' || to.name === 'order-edit') && !canManageOrders()) {
    return { name: 'orders' }
  }
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'login' }
  }
})

export default router
