<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900">
    <div class="bg-white/20 backdrop-blur-lg rounded-xl shadow-xl p-8 w-full max-w-md border border-blue-400/30">
      <h2 class="text-2xl font-bold text-center text-white mb-6">登录</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-white mb-1">用户名</label>
          <input v-model="form.username" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">密码</label>
          <input v-model="form.password" type="password" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <button type="submit" :disabled="loading" class="w-full py-2 mt-4 rounded bg-blue-500 hover:bg-blue-600 text-white font-bold transition flex items-center justify-center">
          <span v-if="loading" class="animate-spin mr-2 border-2 border-white border-t-transparent rounded-full w-4 h-4"></span>
          {{ loading ? '正在登录...' : '登录' }}
        </button>
      </form>
      <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
      <div class="mt-4 text-center">
        <router-link to="/register" class="text-blue-200 hover:underline">没有账号？去注册</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({ username: '', password: '' })
const msg = ref('')
const msgClass = ref('text-red-500')
const loading = ref(false)

async function onSubmit() {
  msg.value = ''
  loading.value = true
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok && data.token) {
      localStorage.setItem('token', data.token)
      msgClass.value = 'text-green-500'
      msg.value = '登录成功，正在跳转...'
      setTimeout(() => router.push('/'), 1200)
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '登录失败'
    }
  } catch (e) {
    msgClass.value = 'text-red-500'
    msg.value = '网络错误或后端异常'
  } finally {
    loading.value = false
  }
}
</script> 