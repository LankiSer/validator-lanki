<template>
  <div class="app">
    <NavBar />
    <main class="container">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from './components/layout/NavBar.vue'
import AppFooter from './components/layout/AppFooter.vue'
</script>
