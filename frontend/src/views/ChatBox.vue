<template>
  <div class="max-w-3xl mx-auto py-8">
    <h2 class="text-2xl text-white font-bold mb-6">即时聊天</h2>
    <div class="mb-4 flex space-x-4">
      <input v-model="targetId" placeholder="对方用户ID或群ID" class="px-3 py-2 rounded bg-white/60 focus:outline-none" />
      <select v-model="chatType" class="px-2 py-2 rounded bg-white/60">
        <option value="private">私信</option>
        <option value="group">群聊</option>
      </select>
      <button @click="onJoin" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">进入</button>
    </div>
    <div v-if="messages.length === 0" class="text-center text-gray-400">暂无消息</div>
    <div v-else class="bg-white/10 rounded-xl p-4 mb-4 max-h-96 overflow-y-auto">
      <div v-for="(msg, idx) in messages" :key="idx" class="mb-2">
        <span class="text-xs text-gray-300">{{ msg.timestamp }}</span>
        <span class="ml-2 text-blue-200" v-if="msg.from">[{{ msg.from }}]</span>
        <span class="ml-2 text-green-200" v-if="msg.group_id">[群{{ msg.group_id }}]</span>
        <span class="ml-2 text-white">{{ msg.content }}</span>
      </div>
    </div>
    <form @submit.prevent="onSend" class="flex space-x-2">
      <input v-model="input" class="flex-1 px-3 py-2 rounded bg-white/60 focus:outline-none" placeholder="输入消息..." />
      <button type="submit" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">发送</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { io, Socket } from 'socket.io-client'

const userId = getUserIdFromToken()
const socket = ref<Socket|null>(null)
const targetId = ref('')
const chatType = ref<'private'|'group'>('private')
const messages = ref<any[]>([])
const input = ref('')

function getUserIdFromToken() {
  const token = localStorage.getItem('token')
  if (!token) return null
  try {
    return JSON.parse(atob(token.split('.')[1])).user_id
  } catch { return null }
}

function connectSocket() {
  if (socket.value) return
  socket.value = io('/', { transports: ['websocket'] })
  socket.value.on('private_message', (msg: any) => {
    messages.value.push(msg)
  })
  socket.value.on('group_message', (msg: any) => {
    messages.value.push(msg)
  })
  // 加入自己的私信房间，接收离线消息
  socket.value.emit('join_user', { user_id: userId })
}

function onJoin() {
  if (!socket.value) connectSocket()
  if (chatType.value === 'group') {
    socket.value?.emit('join_group', { group_id: targetId.value })
  }
  messages.value = []
}

function onSend() {
  if (!input.value.trim()) return
  if (chatType.value === 'private') {
    socket.value?.emit('private_message', {
      sender_id: userId,
      receiver_id: targetId.value,
      content: input.value
    })
  } else {
    socket.value?.emit('group_message', {
      sender_id: userId,
      group_id: targetId.value,
      content: input.value
    })
  }
  messages.value.push({ from: userId, content: input.value, timestamp: new Date().toLocaleString() })
  input.value = ''
}

onMounted(() => {
  connectSocket()
})

onUnmounted(() => {
  socket.value?.disconnect()
})
</script> 