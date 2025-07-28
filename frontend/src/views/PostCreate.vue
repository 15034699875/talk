<template>
  <div class="max-w-2xl mx-auto py-8">
    <TechBlogCard>
      <h2 class="text-xl font-bold text-white mb-4">发布新帖子</h2>
      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-white mb-1">标题</label>
          <input v-model="form.title" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <div>
          <label class="block text-white mb-1">内容（支持Markdown）</label>
          <textarea v-model="form.content" rows="8" class="w-full px-3 py-2 rounded bg-white/60 focus:outline-none" required />
        </div>
        <button type="submit" :disabled="loading" class="w-full py-2 rounded bg-blue-500 hover:bg-blue-600 text-white font-bold transition">{{ loading ? '发布中...' : '发布' }}</button>
      </form>
      <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
    </TechBlogCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TechBlogCard from '../components/TechBlogCard.vue'

const router = useRouter()
const form = ref({ title: '', content: '' })
const msg = ref('')
const msgClass = ref('text-red-500')
const loading = ref(false)

function getToken() {
  return localStorage.getItem('token') || ''
}

async function onSubmit() {
  msg.value = ''
  loading.value = true
  try {
    const res = await fetch('/api/post', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken()
      },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok) {
      msgClass.value = 'text-green-500'
      msg.value = '发布成功，正在跳转...'
      setTimeout(() => router.push('/post'), 1200)
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '发布失败'
    }
  } catch (e) {
    msgClass.value = 'text-red-500'
    msg.value = '网络错误或后端异常'
  } finally {
    loading.value = false
  }
}
</script> 