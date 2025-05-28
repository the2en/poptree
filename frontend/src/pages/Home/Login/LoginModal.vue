<template>
  <div class="login-modal">
    <div class="modal-bg" @click="$emit('close')"></div>
    <div class="modal-content">
      <LoginInbody />
      <button class="close-btn" @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoginInbody from './LoginInbody.vue'
</script>

<style scoped>
.login-modal {
  position: fixed; left: 0; top: 0; width: 100vw; height: 100vh;
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
  color: #222;
}
.modal-bg {
  position: absolute; left: 0; top: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.3);
}
.modal-content {
  position: relative;
  background: #fff;
  border-radius: 16px;
  padding: 32px 24px;
  min-width: 350px;
  z-index: 1;
  font-family: inherit;
  color: inherit;
}
.close-btn {
  margin-top: 16px;
  width: 100%;
  background: #eee;
  border: none;
  border-radius: 8px;
  padding: 8px 0;
  font-size: 1rem;
  cursor: pointer;
  font-family: inherit;
  color: inherit;
}
</style> 