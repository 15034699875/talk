<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900">
    <div class="bg-white/20 backdrop-blur-lg rounded-xl shadow-xl p-8 w-full max-w-md border border-blue-400/30">
      <h2 class="text-2xl font-bold text-center text-white mb-6">注册账号</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-white mb-1">用户名</label>
          <input v-model="form.username" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">邮箱</label>
          <input v-model="form.email" type="email" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">密码</label>
          <input v-model="form.password" type="password" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">确认密码</label>
          <input v-model="form.confirm" type="password" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <button type="submit" :disabled="loading" class="w-full py-2 mt-4 rounded bg-blue-500 hover:bg-blue-600 text-white font-bold transition flex items-center justify-center">
          <span v-if="loading" class="animate-spin mr-2 border-2 border-white border-t-transparent rounded-full w-4 h-4"></span>
          {{ loading ? '正在注册...' : '注册' }}
        </button>
      </form>
      <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
      <div class="mt-4 text-center">
        <router-link to="/login" class="text-blue-200 hover:underline">已有账号？去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({ username: '', email: '', password: '', confirm: '' })
const msg = ref('')
const msgClass = ref('text-red-500')
const loading = ref(false)

async function onSubmit() {
  msg.value = ''
  if (form.value.password !== form.value.confirm) {
    msg.value = '两次密码不一致'
    msgClass.value = 'text-red-500'
    return
  }
  loading.value = true
  try {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: form.value.username,
        password: form.value.password,
        email: form.value.email
      })
    })
    const data = await res.json()
    if (res.ok) {
      msgClass.value = 'text-green-500'
      msg.value = '注册成功，正在跳转登录...'
      setTimeout(() => router.push('/login'), 1200)
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '注册失败'
    }
  } catch (e) {
    msgClass.value = 'text-red-500'
    msg.value = '网络错误或后端异常'
  } finally {
    loading.value = false
  }
}
</script> 