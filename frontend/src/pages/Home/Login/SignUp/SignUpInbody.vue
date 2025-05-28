<template>
  <div class="signup-inbody">
    <div class="logo-title">PopTree</div>
    <form class="form-area" @submit="handleSignUp">
      <div class="input-group">
        <div class="input-wrapper">
          <input id="signup-username" v-model="username" type="text" placeholder="아이디" @blur="validateUsername" />
        </div>
        <div v-if="usernameError" class="error-msg">{{ usernameError }}</div>
        <div class="input-wrapper">
          <input id="signup-name" v-model="name" type="text" placeholder="이름" @blur="validateName" />
        </div>
        <div v-if="nameError" class="error-msg">{{ nameError }}</div>
        <div class="input-wrapper">
          <input id="signup-email" v-model="email" type="email" placeholder="이메일" @blur="validateEmail" />
        </div>
        <div v-if="emailError" class="error-msg">{{ emailError }}</div>
        <div class="input-wrapper">
          <input id="signup-password" v-model="password" type="password" placeholder="비밀번호" @blur="validatePassword" />
        </div>
        <div v-if="passwordError" class="error-msg">{{ passwordError }}</div>
        <div class="input-wrapper">
          <input id="signup-password2" v-model="password2" type="password" placeholder="비밀번호 확인" @blur="validatePassword2" />
        </div>
        <div v-if="password2Error" class="error-msg">{{ password2Error }}</div>
        
        <div v-if="!mydataConsentDone" class="consent-helper">마이데이터 약관 동의 후 회원가입이 가능합니다.</div>
        <div class="mydata-btn-row">
          <button :class="['mydata-btn', mydataConsentDone ? 'mydata-btn-done' : 'mydata-btn-undone']" type="button" @click="goToMyDataConsent">마이데이터 약관 동의</button>
        </div>
        <button class="signup-btn" type="submit" :disabled="!mydataConsentDone">회원가입</button>
      </div>
    </form>
    <MyDataConsentModal :isOpen="showConsentModal" @close="showConsentModal = false" @consent-done="onConsentDone" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MyDataConsentModal from '../MyDataConsent/MyDataConsentModal.vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'

const router = useRouter()
const username = ref('')
const name = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const nameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const password2Error = ref('')
const mydataConsentDone = ref(false)
const showConsentModal = ref(false)
const usernameError = ref('')

function validateName() {
  if (!/^[a-zA-Z가-힣]{2,10}$/.test(name.value)) {
    nameError.value = '이름은 2~10자의 한글 또는 영문만 입력 가능합니다.'
    return false
  }
  nameError.value = ''
  return true
}
function validateEmail() {
  if (!/^[\w-.]+@([\w-]+\.)+[\w-]{2,}$/.test(email.value)) {
    emailError.value = '올바른 이메일 형식이 아닙니다.'
    return false
  }
  emailError.value = ''
  return true
}
function validatePassword() {
  if (!/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=])[A-Za-z\d!@#$%^&*()_+\-=]{8,20}$/.test(password.value)) {
    passwordError.value = '비밀번호는 8~20자, 영문/숫자/특수문자를 포함해야 합니다.'
    return false
  }
  passwordError.value = ''
  return true
}
function validatePassword2() {
  if (password.value !== password2.value) {
    password2Error.value = '비밀번호가 일치하지 않습니다.'
    return false
  }
  password2Error.value = ''
  return true
}
function validateUsername() {
  if (!/^[a-zA-Z0-9가-힣_]{2,15}$/.test(username.value)) {
    usernameError.value = '닉네임은 2~15자의 한글, 영문, 숫자, 언더스코어만 가능합니다.'
    return false
  }
  usernameError.value = ''
  return true
}
function handleSignUp(e: Event) {
  e.preventDefault()
  if (!validateUsername()) {
    document.getElementById('signup-username')?.focus()
    return
  }
  if (!validateName()) {
    document.getElementById('signup-name')?.focus()
    return
  }
  if (!validateEmail()) {
    document.getElementById('signup-email')?.focus()
    return
  }
  if (!validatePassword()) {
    document.getElementById('signup-password')?.focus()
    return
  }
  if (!validatePassword2()) {
    document.getElementById('signup-password2')?.focus()
    return
  }
  // 회원가입 API 연동
  axios.post(`${API_BASE_URL}/api/accounts/auth/signup/`, {
      username: username.value,
      email: email.value,
      name: name.value,
      password1: password.value,
      password2: password2.value
  })
    .then(res => {
      if (!res.ok) return res.json().then(err => { throw err })
      return res.json()
    })
    .then(() => {
      alert('회원가입이 완료되었습니다!')
      router.push('/login')
    })
    .catch(err => {
      // 에러 메시지 표시
      let msg = '회원가입 실패';
      if (err && typeof err === 'object') {
        msg = Object.values(err).flat().join('\n')
      }
      alert(msg)
    })
}
function goToMyDataConsent() {
  showConsentModal.value = true
}
function goBack() {
  router.back()
}
function onConsentDone() {
  mydataConsentDone.value = true
  showConsentModal.value = false
}
</script>

<style scoped>
.signup-inbody {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 24px 0;
  box-sizing: border-box;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
  color: #222;
}
.logo-title {
  font-size: 2.1rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: #3a4344;
  margin-bottom: 48px;
  margin-top: 24px;
  text-align: center;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
}
.form-area {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}
.input-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.input-wrapper {
  position: relative;
  width: 100%;
}
.input-wrapper input {
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 2px solid #ccc;
  outline: none;
  padding: 16px 32px 16px 0;
  font-size: 1.1rem;
  background: transparent;
  color: #222;
  letter-spacing: 1px;
  font-family: inherit;
}
.input-wrapper input::placeholder {
  color: #aaa;
  font-size: 1rem;
  letter-spacing: 1px;
  font-family: inherit;
}
.signup-btn {
  width: 100%;
  background: #222;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 16px 0;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 64px;
  cursor: pointer;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.mydata-btn {
  width: 100%;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 16px 0;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 16px;
  cursor: pointer;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.error-msg {
  color: #e74c3c;
  font-size: 0.95rem;
  margin-top: 4px;
  margin-bottom: 0;
  min-height: 20px;
  font-family: inherit;
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
.mydata-btn-row {
  display: flex;
  align-items: center;
  width: 100%;
}
.mydata-btn {
  flex: 1;
}
.mydata-btn-done {
  background: #1976d2 !important;
  color: #fff !important;
}
.mydata-btn-undone {
  background: #ccc !important;
  color: #fff !important;
  cursor: pointer;
}
.consent-helper {
  margin-top: 12px;
  color: #888;
  font-size: 0.98rem;
  text-align: center;
}
</style> 