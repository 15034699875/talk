<template>
  <div class="max-w-3xl mx-auto py-8">
    <h2 class="text-2xl text-white font-bold mb-6">积分商城</h2>
    <div v-if="loading" class="text-center text-gray-300">加载中...</div>
    <div v-else>
      <div v-if="items.length === 0" class="text-center text-gray-400">暂无可兑换商品</div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="item in items" :key="item.id" class="bg-white/20 backdrop-blur-lg rounded-xl shadow-xl p-6 border border-blue-400/30 flex flex-col">
          <div class="text-lg font-bold text-white mb-2">{{ item.name }}</div>
          <div class="text-gray-200 mb-2">{{ item.description }}</div>
          <div class="text-blue-300 mb-2">所需积分：{{ item.points }}</div>
          <div class="text-xs text-gray-400 mb-2">库存：{{ item.stock }}</div>
          <button @click="onOrder(item)" :disabled="ordering" class="mt-auto px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded">兑换</button>
        </div>
      </div>
      <div v-if="msg" :class="msgClass" class="mt-4 text-center">{{ msg }}</div>
      <div class="mt-10">
        <h3 class="text-xl text-white font-bold mb-4">我的兑换记录</h3>
        <div v-if="ordersLoading" class="text-center text-gray-300">加载中...</div>
        <div v-else-if="orders.length === 0" class="text-center text-gray-400">暂无兑换记录</div>
        <ul v-else class="divide-y divide-blue-200/30">
          <li v-for="o in orders" :key="o.id" class="py-2 flex flex-col md:flex-row md:items-center md:justify-between text-white">
            <span>{{ o.item_name }}</span>
            <span class="text-xs text-gray-300 ml-2">{{ o.created_at }}</span>
            <span v-if="o.download_url" class="ml-2"><a :href="o.download_url" target="_blank" class="text-blue-400 underline">下载</a></span>
            <span v-else class="ml-2 text-gray-400">无下载</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const items = ref<any[]>([])
const loading = ref(true)
const ordering = ref(false)
const msg = ref('')
const msgClass = ref('text-green-500')
const orders = ref<any[]>([])
const ordersLoading = ref(false)

function getToken() {
  return localStorage.getItem('token') || ''
}

async function fetchItems() {
  loading.value = true
  try {
    const res = await fetch('/api/shop/items')
    if (res.ok) {
      items.value = await res.json()
    }
  } finally {
    loading.value = false
  }
}

async function fetchOrders() {
  ordersLoading.value = true
  try {
    const res = await fetch('/api/shop/orders', {
      headers: { 'Authorization': 'Bearer ' + getToken() }
    })
    if (res.ok) {
      orders.value = await res.json()
    }
  } finally {
    ordersLoading.value = false
  }
}

async function onOrder(item: any) {
  msg.value = ''
  ordering.value = true
  try {
    const res = await fetch('/api/shop/order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken()
      },
      body: JSON.stringify({ item_id: item.id })
    })
    const data = await res.json()
    if (res.ok) {
      msgClass.value = 'text-green-500'
      msg.value = '兑换成功！'
      fetchItems()
      fetchOrders()
    } else {
      msgClass.value = 'text-red-500'
      msg.value = data.msg || '兑换失败'
    }
  } finally {
    ordering.value = false
  }
}

onMounted(() => {
  fetchItems()
  fetchOrders()
})
</script> 