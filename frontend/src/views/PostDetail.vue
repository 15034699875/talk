<template>
  <div class="max-w-3xl mx-auto py-8">
    <TechBlogCard v-if="post">
      <div class="flex items-center mb-2">
        <div class="text-2xl font-bold text-white flex-1">{{ post.title }}</div>
        <button v-if="token" @click="onLike" class="ml-4 flex items-center px-3 py-1 rounded bg-pink-500 hover:bg-pink-600 text-white font-bold">
          <span v-if="liked">♥</span><span v-else>♡</span>
          <span class="ml-1">{{ likeCount }}</span>
        </button>
        <span v-else class="ml-4 text-pink-300">♥ {{ likeCount }}</span>
      </div>
      <div class="text-gray-200 mb-2">作者：{{ post.author }} | {{ post.created_at }}</div>
      <div class="prose prose-invert max-w-none text-white" v-html="renderedContent"></div>
    </TechBlogCard>
    <div class="mt-8">
      <h3 class="text-xl text-white font-bold mb-4">评论</h3>
      <div v-if="token" class="mb-6">
        <form @submit.prevent="onSubmit" class="flex space-x-2">
          <input v-model="comment" class="flex-1 px-3 py-2 rounded bg-white/60 focus:outline-none" placeholder="写下你的评论..." required />
          <button type="submit" :disabled="loading" class="px-4 py-2 bg-blue-500 text-white rounded">{{ loading ? '发布中...' : '评论' }}</button>
        </form>
        <div v-if="msg" :class="msgClass" class="mt-2">{{ msg }}</div>
      </div>
      <div v-else class="text-gray-300 mb-4">请先登录后评论。</div>
      <div v-if="comments.length === 0" class="text-gray-400">暂无评论</div>
      <div v-for="c in comments" :key="c.id" class="bg-white/10 rounded p-3 my-2 flex items-center">
        <div class="flex-1">
          <div class="text-white">{{ c.content }}</div>
          <div class="text-xs text-gray-400 mt-1">{{ c.author }} | {{ c.created_at }}</div>
        </div>
        <button v-if="token" @click="onCommentLike(c)" class="ml-4 flex items-center px-2 py-1 rounded bg-pink-500 hover:bg-pink-600 text-white font-bold">
          <span v-if="c.liked">♥</span><span v-else>♡</span>
          <span class="ml-1">{{ c.likeCount }}</span>
        </button>
        <span v-else class="ml-4 text-pink-300">♥ {{ c.likeCount }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import TechBlogCard from '../components/TechBlogCard.vue'
import { marked } from 'marked'

const route = useRoute()
const post = ref<any>(null)
const comments = ref<any[]>([])
const comment = ref('')
const loading = ref(false)
const msg = ref('')
const msgClass = ref('text-green-500')
const token = localStorage.getItem('token')

const likeCount = ref(0)
const liked = ref(false)

const renderedContent = computed(() => post.value ? marked.parse(post.value.content || '') : '')

async function fetchPost() {
  const res = await fetch(`/api/post`)
  if (res.ok) {
    const list = await res.json()
    post.value = list.find((p: any) => p.id === Number(route.params.id))
  }
}

async function fetchLike() {
  const res = await fetch(`/api/like/count?target_type=post&target_id=${route.params.id}`)
  if (res.ok) {
    likeCount.value = (await res.json()).count
  }
}

async function onLike() {
  if (!token) return
  const res = await fetch('/api/like', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({ target_type: 'post', target_id: route.params.id })
  })
  const data = await res.json()
  if (res.ok) {
    likeCount.value = data.count
    liked.value = data.action === 'like'
  }
}

async function fetchComments() {
  const res = await fetch(`/api/comment/${route.params.id}`)
  if (res.ok) {
    const list = await res.json()
    // 拉取每条评论的点赞数
    for (const c of list) {
      const likeRes = await fetch(`/api/like/count?target_type=comment&target_id=${c.id}`)
      c.likeCount = likeRes.ok ? (await likeRes.json()).count : 0
      c.liked = false // 可扩展：后端返回当前用户是否已点赞
    }
    comments.value = list
  }
}

async function onCommentLike(c: any) {
  if (!token) return
  const res = await fetch('/api/like', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({ target_type: 'comment', target_id: c.id })
  })
  const data = await res.json()
  if (res.ok) {
    c.likeCount = data.count
    c.liked = data.action === 'like'
  }
}

async function onSubmit() {
  msg.value = ''
  loading.value = true
  try {
    const res = await fetch(`/api/comment/${route.params.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({ content: comment.value })
    })
    const data = await res.json()
    if (res.ok) {
      msgClass.value = 'text-green-500'
      msg.value = '评论成功'
      comment.value = ''
      fetchComments()
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '评论失败'
    }
  } catch (e) {
    msgClass.value = 'text-red-500'
    msg.value = '网络错误或后端异常'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPost()
  fetchLike()
  fetchComments()
})
</script> 