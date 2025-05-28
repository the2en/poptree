<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">{{ title }}</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <div class="modal-body">
        <p class="modal-text-area">
          {{ content }}
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary modal-close-btn" @click="$emit('close')">확인</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  title: String,
  content: String,
});
const emits = defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.6);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px; margin-bottom: 15px;
}
.modal-title {
  font-size: 1.4rem; font-weight: 600; color: #333; margin: 0;
}
.close-button {
  background: none; border: none; font-size: 2rem; cursor: pointer; color: #888; padding: 0; line-height: 1;
}
.close-button:hover { color: #333; }
.modal-body {
  flex-grow: 1; overflow-y: auto; padding-right: 10px; line-height: 1.6; font-size: 0.95rem; color: #444;
}
.modal-text-area { white-space: pre-wrap; margin: 0; }
.modal-footer {
  padding-top: 15px; border-top: 1px solid #eee; margin-top: 15px; text-align: center;
}
.modal-close-btn {
  width: 100%; padding: 12px 0; border-radius: 24px; font-size: 1rem;
}
</style> 