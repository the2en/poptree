<template>
  <div class="app-container">
    <HeaderBar v-if="showHeader" />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import HeaderBar from '@/components/layout/HeaderBar.vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const route = useRoute()
const showHeader = !['/login', '/signup', '/mydata-consent'].includes(route.path)

const auth = useAuthStore()
onMounted(() => {
  const token = localStorage.getItem('token')
  if (token && !auth.token) {
    auth.setToken(token)
  }
})
</script>

<style>
.app-container {
  width: 100vw;
  max-width: 100vw;
  min-width: 0;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  background: #ffffff;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

body {
  margin: 0;
  padding: 0;
}
</style> 