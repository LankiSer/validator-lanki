import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { getRole, setGuest } from './store/auth'
import './assets/style.css'

if (!getRole()) {
  setGuest()
}

createApp(App).use(router).mount('#app')
