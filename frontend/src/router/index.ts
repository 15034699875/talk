import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/db-setup',
    name: 'DatabaseSetup',
    component: () => import('../views/DatabaseSetup.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/user',
    name: 'UserProfile',
    component: () => import('../views/UserProfile.vue')
  },
  {
    path: '/post',
    name: 'PostList',
    component: () => import('../views/PostList.vue')
  },
  {
    path: '/post/create',
    name: 'PostCreate',
    component: () => import('../views/PostCreate.vue')
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetail.vue')
  },
  {
    path: '/shop',
    name: 'PointsShop',
    component: () => import('../views/PointsShop.vue')
  },
  {
    path: '/group',
    name: 'GroupPanel',
    component: () => import('../views/GroupPanel.vue')
  },
  {
    path: '/chat',
    name: 'ChatBox',
    component: () => import('../views/ChatBox.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 