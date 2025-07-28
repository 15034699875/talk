<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900">
    <h1 class="text-4xl text-white font-bold mb-8">欢迎来到技术博客论坛</h1>
    <div class="flex space-x-4">
      <router-link to="/login" class="px-6 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600">登录</router-link>
      <router-link to="/register" class="px-6 py-2 bg-green-500 text-white rounded shadow hover:bg-green-600">注册</router-link>
      <router-link to="/user" class="px-6 py-2 bg-gray-500 text-white rounded shadow hover:bg-gray-600">个人中心</router-link>
    </div>
  </div>
</template> 