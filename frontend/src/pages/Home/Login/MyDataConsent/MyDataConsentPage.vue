<template>
  <div class="mydata-consent-inbody">
    <div class="logo-title">PopTree</div>
    <form class="form-area" @submit.prevent="goToNextStep">
      <div class="agreement-group all-terms-group">
        <label class="checkbox-container group-header">
          <input type="checkbox" class="checkbox-input" v-model="allTermsAgreed" />
          <span class="checkbox-checkmark"></span>
          <span class="checkbox-label group-title">약관 전체 동의</span>
        </label>
      </div>
      <div class="agreement-group">
        <div class="group-header">
          <span class="group-title-label">필수 동의 항목</span>
        </div>
        <div class="group-items">
          <div v-for="(term, idx) in requiredTerms" :key="idx" class="agreement-item">
            <label class="checkbox-container">
              <input type="checkbox" class="checkbox-input" v-model="term.agreed" />
              <span class="checkbox-checkmark"></span>
              <span class="checkbox-label">{{ term.title }} <span class="required-badge">(필수)</span></span>
            </label>
            <a href="#" class="text-link detail-link" @click.prevent="openModal(term)">자세히 보기 &gt;</a>
          </div>
        </div>
      </div>
      <div class="agreement-group">
        <div class="group-header">
          <span class="group-title-label">선택 동의 항목</span>
        </div>
        <div class="group-items">
          <div v-for="(term, idx) in optionalTerms" :key="idx" class="agreement-item">
            <label class="checkbox-container">
              <input type="checkbox" class="checkbox-input" v-model="term.agreed" />
              <span class="checkbox-checkmark"></span>
              <span class="checkbox-label">{{ term.title }}</span>
            </label>
            <a href="#" class="text-link detail-link" @click.prevent="openModal(term)">자세히 보기 &gt;</a>
          </div>
        </div>
      </div>
      <p class="important-notice-text">※ 필수 동의를 해야만 서비스 이용이 가능합니다.</p>
      <button class="btn btn-primary next-button" type="submit" :disabled="!canProceedToNextStep">동의하고 다음</button>
    </form>
    <MyDataTermsModal
      :isOpen="isModalOpen"
      :title="modalContent.title"
      :content="modalContent.content"
      @close="closeModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import MyDataTermsModal from './MyDataTermsModal.vue'

interface Term {
  title: string;
  content: string;
  required: boolean;
  agreed: boolean;
}

const requiredTerms: Term[] = reactive([
  { title: '개인(신용)정보 수집 및 이용 동의', content: '개인(신용)정보를 수집 및 이용하는 목적, 항목 등에 대한 약관 내용...', required: true, agreed: false },
  { title: '개인(신용)정보 조회 동의', content: '개인(신용)정보를 조회하는 목적, 항목 등에 대한 약관 내용...', required: true, agreed: false },
])
const optionalTerms: Term[] = reactive([
  { title: '마케팅 정보 수신 동의', content: '마케팅 목적의 정보를 수신하는 것에 대한 약관 내용...', required: false, agreed: false },
  { title: '제3자 정보 제공 동의', content: '서비스 제공을 위해 제3자에게 정보를 제공하는 것에 대한 약관 내용...', required: false, agreed: false },
])
const allTermsAgreed = computed({
  get: () => requiredTerms.every(term => term.agreed) && optionalTerms.every(term => term.agreed),
  set: (value: boolean) => {
    requiredTerms.forEach(term => { term.agreed = value })
    optionalTerms.forEach(term => { term.agreed = value })
  }
})
const allRequiredTermsAgreed = computed(() => requiredTerms.every(term => term.agreed))
const canProceedToNextStep = computed(() => allRequiredTermsAgreed.value)

const isModalOpen = ref(false)
const modalContent = reactive({ title: '', content: '' })
function openModal(term: Term) {
  modalContent.title = term.title
  modalContent.content = term.content
  isModalOpen.value = true
}
function closeModal() {
  isModalOpen.value = false
  modalContent.title = ''
  modalContent.content = ''
}
function goToNextStep() {
  if (!canProceedToNextStep.value) return
  // 동의 완료 시 localStorage에 플래그 저장 후 회원가입 페이지로 이동
  localStorage.setItem('mydataConsentDone', 'true')
  window.location.href = '/signup'
}
</script>

<style scoped>
.mydata-consent-inbody {
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
  justify-content: flex-start;
  position: relative;
  padding: 32px 20px;
  box-sizing: border-box;
  margin: 0 auto;
  gap: 12px;
}
.logo-title {
  font-size: 2.4rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: #3a4344;
  margin-bottom: 32px;
  margin-top: 0;
  text-align: center;
}
.form-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}
.agreement-group {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  margin-bottom: 12px;
}
.agreement-group.all-terms-group {
  border: none;
  margin-bottom: 10px;
  background: none;
}
.group-header {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  font-weight: 600;
  font-size: 1.05rem;
}
.group-title-label {
  padding-left: 30px;
}
.group-items {
  padding: 0 16px;
}
.agreement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}
.agreement-item:last-child {
  border-bottom: none;
}
.required-badge {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-left: 4px;
  font-weight: normal;
}
.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}
.checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}
.checkbox-checkmark {
  height: 20px;
  width: 20px;
  background-color: #eee;
  border: 1px solid #ccc;
  border-radius: 50%;
  margin-right: 10px;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}
.checkbox-input:checked + .checkbox-checkmark {
  background-color: #007bff;
  border-color: #007bff;
}
.checkbox-checkmark::after {
  content: "✔";
  color: white;
  font-size: 14px;
  display: none;
}
.checkbox-input:checked + .checkbox-checkmark::after {
  display: block;
}
.checkbox-label {
  font-size: 1rem;
  color: #333;
}
.group-title.checkbox-label {
  font-weight: 600;
}
.text-link {
  color: #007bff;
  text-decoration: none;
  font-size: 0.95rem;
  white-space: nowrap;
}
.text-link:hover {
  text-decoration: underline;
}
.important-notice-text {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
  margin-top: 10px;
}
.btn {
  width: 100%;
  padding: 15px 0;
  border: none;
  border-radius: 24px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.btn-primary {
  background-color: #007bff;
  color: white;
}
.btn-primary:disabled {
  background-color: #a0cffc;
  cursor: not-allowed;
}
.next-button {
  margin-top: 30px;
}
</style> 