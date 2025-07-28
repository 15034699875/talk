<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900">
    <div class="bg-white/20 backdrop-blur-lg rounded-xl shadow-xl p-8 w-full max-w-md border border-blue-400/30">
      <h2 class="text-2xl font-bold text-center text-white mb-6">数据库配置</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-white mb-1">主机地址</label>
          <input v-model="form.host" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">端口</label>
          <input v-model="form.port" type="number" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">用户名</label>
          <input v-model="form.user" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">密码</label>
          <input v-model="form.password" type="password" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">数据库名</label>
          <input v-model="form.database" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <button type="submit" :disabled="loading" class="w-full py-2 mt-4 rounded bg-blue-500 hover:bg-blue-600 text-white font-bold transition flex items-center justify-center">
          <span v-if="loading" class="animate-spin mr-2 border-2 border-white border-t-transparent rounded-full w-4 h-4"></span>
          {{ loading ? '正在初始化...' : '提交并初始化' }}
        </button>
      </form>
      <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
      <div v-if="showSuccess" class="fixed inset-0 flex items-center justify-center bg-black/40 z-50">
        <div class="bg-white rounded-lg p-6 shadow-xl text-center">
          <div class="text-green-600 text-2xl mb-2">✔</div>
          <div class="text-lg mb-4">数据库初始化成功！</div>
          <button @click="goHome" class="px-6 py-2 bg-blue-500 text-white rounded">进入首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  host: 'localhost',
  port: 3306,
  user: 'root',
  password: '',
  database: 'talk',
})
const msg = ref('')
const msgClass = ref('text-red-500')
const loading = ref(false)
const showSuccess = ref(false)

async function onSubmit() {
  msg.value = ''
  loading.value = true
  try {
    const res = await fetch('/api/db/init', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (data.success) {
      msgClass.value = 'text-green-500'
      msg.value = '数据库初始化成功！'
      showSuccess.value = true
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '初始化失败'
    }
  } catch (e) {
    msgClass.value = 'text-red-500'
    msg.value = '网络错误或后端异常'
  } finally {
    loading.value = false
  }
}
function goHome() {
  router.push('/')
}
</script> 