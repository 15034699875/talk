<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900">
    <div class="bg-white/20 backdrop-blur-lg rounded-xl shadow-xl p-8 w-full max-w-md border border-blue-400/30">
      <h2 class="text-2xl font-bold text-center text-white mb-6">个人中心</h2>
      <div v-if="loading" class="text-center text-white">加载中...</div>
      <div v-else>
        <div class="flex flex-col items-center mb-4">
          <img :src="user.avatar_url || 'https://api.dicebear.com/7.x/identicon/svg?seed=' + user.username" class="w-20 h-20 rounded-full border-4 border-blue-400 mb-2 bg-white/60" />
          <input v-model="form.avatar_url" placeholder="头像URL" class="w-full px-3 py-1 rounded bg-white/60 focus:outline-none mt-2" />
        </div>
        <div class="mb-2 text-white">用户名：{{ user.username }}</div>
        <div class="mb-2 text-white">邮箱：<input v-model="form.email" class="px-2 py-1 rounded bg-white/60 focus:outline-none" /></div>
        <div class="mb-2 text-white">积分：{{ user.points }} <span class="ml-2 text-xs text-blue-200">经验：{{ user.exp }}</span></div>
        <div class="mb-2 text-white">等级：Lv.{{ level }}</div>
        <div class="mb-2 text-white">角色：{{ user.role }}</div>
        <button @click="onSave" :disabled="saving" class="w-full py-2 mt-4 rounded bg-blue-500 hover:bg-blue-600 text-white font-bold transition">保存修改</button>
        <button @click="onLogout" class="w-full py-2 mt-2 rounded bg-gray-500 hover:bg-gray-600 text-white font-bold transition">退出登录</button>
        <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
        <div class="mt-8">
          <div class="flex space-x-4 justify-center mb-2">
            <button @click="tab='profile'" :class="tab==='profile' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-white'" class="px-4 py-1">基本信息</button>
            <button @click="tab='points'" :class="tab==='points' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-white'" class="px-4 py-1">积分明细</button>
          </div>
          <div v-if="tab==='points'">
            <div v-if="pointLogsLoading" class="text-center text-gray-300">加载中...</div>
            <div v-else-if="pointLogs.length === 0" class="text-center text-gray-400">暂无积分变动</div>
            <ul v-else class="divide-y divide-blue-200/30">
              <li v-for="log in pointLogs" :key="log.id" class="py-2 flex justify-between text-white">
                <span>{{ log.reason }}</span>
                <span :class="log.change > 0 ? 'text-green-400' : 'text-red-400'">{{ log.change > 0 ? '+' : '' }}{{ log.change }}</span>
                <span class="text-xs text-gray-300 ml-2">{{ log.created_at }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref<any>({})
const form = ref({ avatar_url: '', email: '' })
const msg = ref('')
const msgClass = ref('text-green-500')
const loading = ref(true)
const saving = ref(false)
const tab = ref<'profile'|'points'>('profile')

const pointLogs = ref<any[]>([])
const pointLogsLoading = ref(false)

const level = computed(() => Math.floor((user.value.exp || 0) / 1000) + 1)

function getToken() {
  return localStorage.getItem('token') || ''
}

async function fetchProfile() {
  loading.value = true
  try {
    const res = await fetch('/api/user/profile', {
      headers: { 'Authorization': 'Bearer ' + getToken() }
    })
    if (res.status === 401) {
      router.replace('/login')
      return
    }
    const data = await res.json()
    user.value = data
    form.value.avatar_url = data.avatar_url || ''
    form.value.email = data.email || ''
  } catch (e) {
    msg.value = '加载失败'
    msgClass.value = 'text-red-500'
  } finally {
    loading.value = false
  }
}

async function fetchPointLogs() {
  pointLogsLoading.value = true
  try {
    const res = await fetch('/api/user/points/logs', {
      headers: { 'Authorization': 'Bearer ' + getToken() }
    })
    if (res.ok) {
      pointLogs.value = await res.json()
    }
  } finally {
    pointLogsLoading.value = false
  }
}

async function onSave() {
  saving.value = true
  msg.value = ''
  try {
    const res = await fetch('/api/user/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken()
      },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok) {
      msg.value = '保存成功'
      msgClass.value = 'text-green-500'
      fetchProfile()
    } else {
      msg.value = data.msg || '保存失败'
      msgClass.value = 'text-red-500'
    }
  } catch (e) {
    msg.value = '网络错误或后端异常'
    msgClass.value = 'text-red-500'
  } finally {
    saving.value = false
  }
}

function onLogout() {
  localStorage.removeItem('token')
  router.replace('/login')
}

onMounted(() => {
  fetchProfile()
  fetchPointLogs()
})
</script> 