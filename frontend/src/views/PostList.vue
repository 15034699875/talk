<template>
  <div class="max-w-3xl mx-auto py-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl text-white font-bold">最新帖子</h2>
      <router-link to="/post/create" class="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600">发帖</router-link>
    </div>
    <div class="space-y-4">
      <router-link v-for="post in posts" :key="post.id" :to="`/post/${post.id}`" class="block">
        <TechBlogCard>
          <div class="text-lg font-bold text-white">{{ post.title }}</div>
          <div class="text-gray-200 mt-2">{{ post.summary }}</div>
          <div class="text-xs text-gray-400 mt-2">作者：{{ post.author }} | {{ post.created_at }}</div>
        </TechBlogCard>
      </router-link>
      <div v-if="posts.length === 0" class="text-center text-gray-400">暂无帖子</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import TechBlogCard from '../components/TechBlogCard.vue'

const posts = ref<any[]>([])

async function fetchPosts() {
  const res = await fetch('/api/post')
  if (res.ok) {
    posts.value = await res.json()
  }
}

onMounted(fetchPosts)
</script> 