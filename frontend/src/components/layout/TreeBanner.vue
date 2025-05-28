<template>
  <div class="tree-banner">
    <div class="banner-text">이번 달 소비가<br />만만치 않다구요</div>
    <div class="tree-img-placeholder">나무 일러스트 자리</div>
  </div>
</template>
<script setup lang="ts"></script>
<style scoped>
.tree-banner {
  background: #eaf7e1;
  border-radius: 16px;
  padding: 24px 16px 0 16px;
  display: flex; flex-direction: column; align-items: center;
  width: 320px; margin: 0 auto 24px auto;
}
.banner-text { font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; text-align: center; }
.tree-img-placeholder {
  width: 180px;
  height: 120px;
  background: #d0e6c6;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7a9c6b;
  font-size: 1.1rem;
  margin-bottom: 8px;
}
</style> 