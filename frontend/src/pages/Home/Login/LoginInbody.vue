<template>
  <div class="login-inbody">
    <div class="logo-title">PopTree</div>
    <form class="form-area" @submit="handleLogin">
      
      <div class="input-group">
        <div class="input-wrapper">
          <input id="login-username" v-model="username" type="text" placeholder="아이디" @blur="validateUsername" />
          <span class="icon user"></span>
        </div>
        <div v-if="usernameError" class="error-msg">{{ usernameError }}</div>
        <div class="input-wrapper">
          <input id="login-password" v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="비밀번호" @blur="validatePassword" />
          <span class="icon eye" @click="togglePasswordVisibility"></span>
        </div>
        <div v-if="passwordError" class="error-msg">{{ passwordError }}</div>
        <button class="login-btn" type="submit" :disabled="loading">
          <span v-if="loading" class="loading-spinner"></span>
          <span v-else>로그인</span>
        </button>
      </div>
    </form>
    <div class="signup-link">
      계정이 없으신가요?
      <a @click.prevent="goToSignUp" href="#">회원가입</a>
    </div>
    <div class="divider"><span>Or</span></div>
    <button class="google-btn">
      <span class="google-icon">
        <svg width="18" height="18" viewBox="0 0 48 48"><g><path fill="#4285F4" d="M43.6 20.5H42V20H24v8h11.3C34.7 32.1 30.1 35 24 35c-6.1 0-11.3-5-11.3-11S17.9 13 24 13c2.6 0 5 .8 6.9 2.3l6.5-6.5C34.6 5.1 29.6 3 24 3 12.4 3 3 12.4 3 24s9.4 21 21 21c10.5 0 19.5-7.5 19.5-21 0-1.4-.1-2.7-.4-4z"/><path fill="#34A853" d="M6.3 14.7l6.6 4.8C14.5 16.1 18.9 13 24 13c2.6 0 5 .8 6.9 2.3l6.5-6.5C34.6 5.1 29.6 3 24 3 15.3 3 7.9 8.7 6.3 14.7z"/><path fill="#FBBC05" d="M24 45c5.6 0 10.6-1.8 14.5-4.9l-6.7-5.5C29.7 36.7 27 37.5 24 37.5c-6.1 0-11.3-5-11.3-11 0-1.7.4-3.3 1.1-4.7l-6.6-5.1C5.1 20.1 3 22.9 3 24c0 11.6 9.4 21 21 21z"/><path fill="#EA4335" d="M43.6 20.5H42V20H24v8h11.3c-1.2 3.2-4.3 5.5-7.3 5.5-6.1 0-11.3-5-11.3-11 0-1.7.4-3.3 1.1-4.7l-6.6-5.1C5.1 20.1 3 22.9 3 24c0 11.6 9.4 21 21 21 10.5 0 19.5-7.5 19.5-21 0-1.4-.1-2.7-.4-4z"/></g></svg>
      </span>
      <span class="google-text">구글로 로그인</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')
const usernameError = ref('')
const passwordError = ref('')
const loading = ref(false)
const showPassword = ref(false)

function validateUsername() {
  if (!username.value) {
    usernameError.value = '아이디를 입력해주세요'
    return false
  }
  usernameError.value = ''
  return true
}
function validatePassword() {
  if (!password.value) {
    passwordError.value = '비밀번호를 입력해주세요'
    return false
  }
  passwordError.value = ''
  return true
}
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}
function handleLogin(e: Event) {
  e.preventDefault()
  const userValid = validateUsername()
  if (!userValid) {
    document.getElementById('login-username')?.focus()
    return
  }
  const passValid = validatePassword()
  if (!passValid) {
    document.getElementById('login-password')?.focus()
    return
  }
  loading.value = true
  // axios 스타일로 수정
  axios.post(`${API_BASE_URL}/api/accounts/auth/login/`, { username: username.value, password: password.value })
    .then(response => {
      auth.setToken(response.data.access)
      if (response.data.user) {
        auth.setUser(response.data.user)
      }
      alert('로그인에 성공했습니다!')
      router.push('/')
    })
    .catch(error => {
      alert('로그인에 실패했습니다: ' + (error.response?.data?.detail || error.message))
    })
    .finally(() => {
      loading.value = false
    })
}
function goToSignUp() {
  router.push('/signup')
}
</script>

<style scoped>
.login-inbody {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 24px 0;
  box-sizing: border-box;
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
}
.input-wrapper input::placeholder {
  color: #aaa;
  font-size: 1rem;
  letter-spacing: 1px;
  font-family: inherit;
}
.icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  opacity: 0.5;
  cursor: pointer;
}
.icon.user::before {
  content: '\1F464';
  font-size: 1.2rem;
}
.icon.eye::before {
  content: '\1F441';
  font-size: 1.2rem;
}
.login-btn, .signup-btn {
  color: #fff !important;
  background: #222;
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
.login-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #fff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.signup-link {
  margin: 24px 0 12px 0;
  font-size: 1rem;
  color: #222;
  text-align: center;
}
.signup-link a {
  color: #1976d2;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  cursor: pointer;
}
.divider {
  width: 100%;
  display: flex;
  align-items: center;
  margin: 18px 0 12px 0;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1.5px;
  background: #eee;
}
.divider span {
  margin: 0 12px;
  color: #aaa;
  font-size: 0.95rem;
}
.google-btn {
  width: 100%;
  background: #fff;
  color: #222;
  border: 1.5px solid #e0e0e0;
  border-radius: 6px;
  padding: 12px 0;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  cursor: pointer;
}
.google-btn:hover {
  background: #f5f5f5;
}
.google-icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.google-text {
  font-size: 1.05rem;
  font-weight: 500;
  color: #222;
  letter-spacing: 0.2px;
}
.error-msg {
  color: #e74c3c;
  font-size: 0.95rem;
  margin-top: 4px;
  margin-bottom: 0;
  min-height: 20px;
}
.login-inbody, .form-area, .input-group, .input-wrapper input, .login-btn, .google-btn, .google-text {
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
  color: #222;
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