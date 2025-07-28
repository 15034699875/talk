import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './assets/tailwind.css'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// 路由守卫：未登录访问/user等受保护页面自动跳转登录
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const publicPages = ['/login', '/register', '/db-setup']
  if (!publicPages.includes(to.path) && !token) {
    return next('/login')
  }
  next()
})

fetch('/api/db/status')
  .then(res => res.json())
  .then(data => {
    if (data && data.initialized === false) {
      router.replace('/db-setup')
    }
    app.use(router).mount('#app')
  })
  .catch(() => {
    app.use(router).mount('#app')
  }) 