<template>
  <div class="login-page">
    <div class="login-card">
      <button class="back-btn" @click="goBack">← 뒤로가기</button>
      <LoginInbody />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import LoginInbody from './LoginInbody.vue'
const router = useRouter()
function goBack() {
  router.back()
}
</script>

<style scoped>
.login-page {
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  position: relative;
}
.login-card {
  width: 100%;
  max-width: 480px;
  min-width: 320px;
  min-height: 480px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 60px 20px;
  box-sizing: border-box;
  margin-top: 100px;
  margin-bottom: 48px;
}
@media (max-width: 600px) {
  .login-card {
    height: auto;
    min-width: 0;
    padding: 32px 8px;
    border-radius: 0;
    box-shadow: none;
  }
}
.back-btn {
  position: absolute;
  top: 24px;
  left: 24px;
  background: none;
  border: none;
  color: #6DB872;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  z-index: 10;
}
</style> 