<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">마이데이터 약관 동의</h3>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      <form class="form-area" @submit.prevent="onConsent">
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
        <button class="btn btn-primary next-button" type="submit" :disabled="!canProceedToNextStep">동의하고 닫기</button>
      </form>
      <MyDataTermsModal
        :isOpen="isModalOpen"
        :title="modalContent.title"
        :content="modalContent.content"
        @close="closeModal"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, defineProps, defineEmits } from 'vue'
import MyDataTermsModal from './MyDataTermsModal.vue'

const props = defineProps({
  isOpen: Boolean
})
const emit = defineEmits(['close', 'consent-done'])

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
function onConsent() {
  if (!canProceedToNextStep.value) return
  emit('consent-done')
  emit('close')
}
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
  border-radius: 18px;
  padding: 32px 32px 28px 32px;
  width: 95%;
  max-width: 540px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1.5px solid #e0e0e0;
  padding-bottom: 18px; margin-bottom: 24px;
}
.modal-title {
  font-size: 2rem; font-weight: 700; color: #222; margin: 0;
}
.close-button {
  background: none; border: none; font-size: 2rem; cursor: pointer; color: #888; padding: 0; line-height: 1;
}
.close-button:hover { color: #1976d2; }
.form-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}
.agreement-group {
  width: 100%;
  border: none;
  border-radius: 0;
  background: none;
  margin-bottom: 28px;
}
.agreement-group.all-terms-group {
  border: none;
  margin-bottom: 18px;
  background: none;
}
.group-header {
  padding: 0 0 10px 0;
  border-bottom: 1.5px solid #e0e0e0;
  display: flex;
  align-items: center;
  background: none;
  font-weight: 600;
  font-size: 1.15rem;
  margin-bottom: 8px;
}
.group-title-label {
  padding-left: 30px;
}
.group-items {
  padding: 0 8px;
}
.agreement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #f0f0f0;
}
.agreement-item:last-child {
  border-bottom: none;
}
.required-badge {
  color: #e74c3c;
  font-size: 0.95rem;
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
  height: 24px;
  width: 24px;
  background-color: #eee;
  border: 1.5px solid #bbb;
  border-radius: 6px;
  margin-right: 12px;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}
.checkbox-input:checked + .checkbox-checkmark {
  background-color: #1976d2;
  border-color: #1976d2;
}
.checkbox-checkmark::after {
  content: "✔";
  color: white;
  font-size: 16px;
  display: none;
}
.checkbox-input:checked + .checkbox-checkmark::after {
  display: block;
}
.checkbox-label {
  font-size: 1.08rem;
  color: #222;
  margin-left: 2px;
}
.group-title.checkbox-label {
  font-weight: 600;
}
.text-link {
  color: #1976d2;
  text-decoration: underline;
  font-size: 1.05rem;
  white-space: nowrap;
  font-weight: 500;
  margin-left: 8px;
  transition: color 0.15s;
}
.text-link:hover {
  color: #1251a3;
  text-decoration: underline;
}
.important-notice-text {
  font-size: 1.05rem;
  color: #555;
  text-align: center;
  margin: 24px 0 0 0;
}
.btn {
  width: 100%;
  padding: 16px 0;
  border: none;
  border-radius: 24px;
  font-size: 1.15rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 18px;
}
.btn-primary {
  background-color: #1976d2;
  color: #fff;
  box-shadow: 0 2px 8px rgba(25,118,210,0.08);
}
.btn-primary:disabled {
  background-color: #b5c7de;
  color: #fff;
  cursor: not-allowed;
}
.next-button {
  margin-top: 0;
}
</style> 