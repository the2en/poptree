<template>
  <div class="ai-recommend-root">
    <button class="ai-recommend-btn" @click="onClick" :disabled="isDisabled">
      <img src="/ai_tree.png" alt="AI 추천" class="ai-tree-img" />
      <span class="ai-recommend-text">AI를 활용해 사용자님께 맞춤 상품을 찾아드려요!</span>
      <span class="ai-recommend-arrow">→</span>
    </button>
    <div v-if="showModal" class="ai-modal-backdrop" @click.self="closeModal">
      <div class="ai-modal">
        <div class="ai-modal-title">
          AI 맞춤 추천 결과
          <template v-if="aiUserName"> <span class="ai-modal-username">{{ aiUserName }}님을 위한 추천</span></template>
        </div>
        <div v-if="loading" class="ai-modal-loading">AI가 답변을 생성 중입니다...</div>
        <div v-else-if="error" class="ai-modal-error">{{ error }}</div>
        <div v-else-if="answer" class="ai-modal-answer-scroll">
          <div class="ai-modal-answer-text">{{ answer }}</div>
        </div>
        <button class="ai-modal-close" @click="closeModal">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showModal = ref(false)
const loading = ref(false)
const answer = ref('')
const error = ref('')
const aiUserName = ref('')

const userId = computed(() => auth.user?.id)
const userName = computed(() => auth.user?.name)
const isDisabled = computed(() => !userId.value)

function onClick() {
  if (isDisabled.value) return
  showModal.value = true
  answer.value = ''
  error.value = ''
  aiUserName.value = ''
  loading.value = true
  axios.post(`${API_BASE_URL}/api/investments/gpt/answer/`, {
    user_id: userId.value,
    user_name: userName.value,
    question: '내 투자 성향에 맞는 금융 상품을 추천해줘'
  })
    .then(res => {
      answer.value = res.data.answer
      aiUserName.value = res.data.user_name
    })
    .catch(e => {
      error.value = e.response?.data?.error || 'AI 추천 요청 실패'
    })
    .finally(() => {
      loading.value = false
    })
}
function closeModal() {
  showModal.value = false
}
</script>

<style scoped>
.ai-recommend-root {
  display: flex;
  justify-content: center;
  margin: 32px 0 0 0;
}
.ai-recommend-btn {
  display: flex;
  align-items: center;
  gap: 18px;
  background: #fffbe9;
  border: 2px solid #1bc47d;
  border-radius: 32px;
  padding: 18px 32px;
  font-size: 20px;
  font-weight: 700;
  color: #1bc47d;
  cursor: pointer;
  box-shadow: 0 2px 12px rgba(27,196,125,0.08);
  transition: background 0.15s, border 0.15s;
}
.ai-recommend-btn:hover {
  background: #e0f7e9;
  border-color: #179e5c;
}
.ai-tree-img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #fff;
  object-fit: contain;
  border: 1.5px solid #1bc47d;
}
.ai-recommend-text {
  font-size: 20px;
  font-weight: 700;
  color: #1bc47d;
}
.ai-recommend-arrow {
  font-size: 28px;
  color: #1bc47d;
  margin-left: 8px;
}
.ai-modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ai-modal {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.13);
  padding: 32px 28px 24px 28px;
  min-width: 340px;
  max-width: 90vw;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ai-modal-title {
  font-size: 22px;
  font-weight: 700;
  color: #1bc47d;
  margin-bottom: 18px;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
}
.ai-modal-username {
  display: inline-block;
  margin-left: 8px;
  color: #1bc47d;
  font-size: 17px;
  font-weight: 600;
}
.ai-modal-loading {
  color: #888;
  font-size: 18px;
  margin-bottom: 18px;
}
.ai-modal-error {
  color: #e23c3c;
  font-size: 17px;
  margin-bottom: 18px;
}
.ai-modal-answer-scroll {
  width: 100%;
  max-width: 540px;
  max-height: 320px;
  overflow-y: auto;
  margin-bottom: 18px;
  background: #f8faf7;
  border-radius: 12px;
  box-shadow: 0 1px 6px rgba(27,196,125,0.06);
  padding: 18px 18px 18px 18px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  max-width: 90vw;
}
.ai-modal-answer-text {
  color: #222;
  font-size: 17px;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
  line-height: 1.8;
  white-space: pre-line;
  word-break: break-word;
  overflow-wrap: break-word;
  letter-spacing: 0.01em;
  padding: 0;
  margin: 0;
  max-width: 90vw;
  box-sizing: border-box;
}
.ai-modal-close {
  margin-top: 8px;
  background: #1bc47d;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.ai-modal-close:hover {
  background: #179e5c;
}
@media (max-width: 600px) {
  .ai-modal-answer-scroll, .ai-modal-answer-text {
    max-width: 98vw;
    font-size: 15px;
    padding: 12px 6px 12px 6px;
  }
}
</style> 