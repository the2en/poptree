<template>
  <div class="signup-page">
    <div class="signup-card">
      <button class="back-btn" @click="$router.back()">← 뒤로가기</button>
      
      <SignUpInbody />
    </div>
  </div>
</template>

<script setup lang="ts">
import SignUpInbody from './SignUpInbody.vue'
</script>

<style scoped>
.signup-page {
  padding-top: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  position: relative;
}
.signup-card {
  width: 100%;
  max-width: 480px;
  min-width: 320px;
  height: 720px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 8px 20px;
  box-sizing: border-box;
  margin-top: 12px;
  margin-bottom: 48px;
}
@media (max-width: 600px) {
  .signup-card {
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