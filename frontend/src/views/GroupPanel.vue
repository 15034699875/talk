<template>
  <div class="max-w-3xl mx-auto py-8">
    <h2 class="text-2xl text-white font-bold mb-6">群组管理</h2>
    <div class="mb-6 flex space-x-4">
      <input v-model="newGroupName" placeholder="新群组名称" class="px-3 py-2 rounded bg-white/60 focus:outline-none" />
      <button @click="onCreateGroup" :disabled="creating" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">创建群组</button>
    </div>
    <div class="mb-6 flex space-x-4">
      <input v-model="searchKey" placeholder="搜索群组" class="px-3 py-2 rounded bg-white/60 focus:outline-none" />
      <button @click="onSearch" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">搜索</button>
    </div>
    <div v-if="groups.length === 0" class="text-center text-gray-400 mb-8">暂无群组</div>
    <div v-else class="space-y-4 mb-8">
      <div v-for="g in groups" :key="g.id" class="bg-white/20 rounded-xl p-4 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <span class="text-lg text-white font-bold">{{ g.name }}</span>
          <span class="ml-2 text-xs text-gray-300">ID:{{ g.id }}</span>
        </div>
        <button @click="onJoin(g)" class="mt-2 md:mt-0 px-4 py-1 bg-green-500 hover:bg-green-600 text-white rounded">加入</button>
        <button @click="onShowMembers(g)" class="mt-2 md:mt-0 px-4 py-1 bg-blue-400 hover:bg-blue-500 text-white rounded">成员</button>
      </div>
    </div>
    <div v-if="showMembers" class="fixed inset-0 flex items-center justify-center bg-black/40 z-50">
      <div class="bg-white rounded-lg p-6 shadow-xl w-full max-w-md">
        <h3 class="text-lg font-bold mb-4">群成员</h3>
        <ul>
          <li v-for="m in members" :key="m.user_id" class="flex justify-between items-center py-2 border-b border-gray-200">
            <span>用户ID: {{ m.user_id }}</span>
            <span class="text-xs text-gray-500">{{ m.role }}</span>
            <template v-if="isOwner && m.role !== 'owner'">
              <select v-model="m.role" @change="onSetRole(m)" class="ml-2 px-2 py-1 rounded bg-gray-100">
                <option value="admin">管理员</option>
                <option value="member">成员</option>
              </select>
            </template>
          </li>
        </ul>
        <button @click="showMembers=false" class="mt-4 px-4 py-2 bg-gray-400 text-white rounded">关闭</button>
      </div>
    </div>
    <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const newGroupName = ref('')
const creating = ref(false)
const searchKey = ref('')
const groups = ref<any[]>([])
const msg = ref('')
const msgClass = ref('text-green-500')
const members = ref<any[]>([])
const showMembers = ref(false)
const currentGroupId = ref<number|null>(null)
const isOwner = ref(false)

function getToken() {
  return localStorage.getItem('token') || ''
}

async function onCreateGroup() {
  if (!newGroupName.value) return
  creating.value = true
  msg.value = ''
  try {
    const res = await fetch('/api/group', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken()
      },
      body: JSON.stringify({ name: newGroupName.value })
    })
    const data = await res.json()
    if (res.ok) {
      msgClass.value = 'text-green-500'
      msg.value = '创建成功'
      onSearch()
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '创建失败'
    }
  } finally {
    creating.value = false
  }
}

async function onSearch() {
  msg.value = ''
  const res = await fetch(`/api/group/search?q=${encodeURIComponent(searchKey.value)}`)
  if (res.ok) {
    groups.value = await res.json()
  }
}

async function onJoin(g: any) {
  msg.value = ''
  const res = await fetch(`/api/group/${g.id}/join`, {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + getToken() }
  })
  const data = await res.json()
  if (res.ok) {
    msgClass.value = 'text-green-500'
    msg.value = '加入成功'
  } else {
    msgClass.value = 'text-red-500'
    msg.value = data.msg || '加入失败'
  }
}

async function onShowMembers(g: any) {
  currentGroupId.value = g.id
  showMembers.value = true
  const res = await fetch(`/api/group/${g.id}/members`)
  if (res.ok) {
    members.value = await res.json()
    // 判断当前用户是否为群主
    const token = getToken()
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]))
      isOwner.value = g.owner_id === payload.user_id
    } else {
      isOwner.value = false
    }
  }
}

async function onSetRole(m: any) {
  if (!currentGroupId.value) return
  const res = await fetch(`/api/group/${currentGroupId.value}/set_role`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getToken()
    },
    body: JSON.stringify({ user_id: m.user_id, role: m.role })
  })
  const data = await res.json()
  if (res.ok) {
    msgClass.value = 'text-green-500'
    msg.value = '角色已更新'
  } else {
    msgClass.value = 'text-red-500'
    msg.value = data.msg || '操作失败'
  }
}
</script> 