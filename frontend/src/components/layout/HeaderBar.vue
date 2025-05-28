<template>
  <header class="main-header" :class="{ 'scrolled': isHeaderScrolled }">
    <div class="header-inner">
      <slot name="left">
        <router-link to="/" class="logo-link" aria-label="홈으로 이동">
          <div class="logo">Pop Tree</div>
        </router-link>
      </slot>
      <button 
        class="mobile-nav-toggle" 
        @click="toggleMobileNav" 
        aria-label="네비게이션 메뉴 열기/닫기" 
        :aria-expanded="isMobileNavOpen"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
      <nav 
        :class="{ 'mobile-nav-open': isMobileNavOpen }" 
        v-if="!hideNav || isMobileNavOpen"
      >
        <router-link to="/">홈</router-link>
        <router-link to="/invest">투자정보</router-link>
        <router-link to="/ranking">랭킹</router-link>
        <template v-if="auth.isLoggedIn">
          <button class="header-btn logout-btn" @click="auth.logout">로그아웃</button>
          <button class="header-btn withdraw-btn" @click="auth.withdraw">회원탈퇴</button>
        </template>
        <template v-else>
          <button class="header-btn login-btn" @click="goToLogin">로그인</button>
          <button class="header-btn signup-btn" @click="goToSignUp">회원가입</button>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  hideNav: Boolean
})

const isMobileNavOpen = ref(false)
const isHeaderScrolled = ref(false)
const router = useRouter()
const auth = useAuthStore()

const toggleMobileNav = () => {
  isMobileNavOpen.value = !isMobileNavOpen.value
}

const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 50
}

function goToLogin() {
  router.push('/login')
}

function goToSignUp() {
  router.push('/signup')
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
:root {
  /* Colors */
  --main-green: #6DB872;
  --text-primary: #333;
  --bg-hover-light: #f5f5f5;
  --bg-active-light: #eaf7ef;
  --header-bg: rgba(255,255,255,0.96);
  
  /* Layout */
  --content-max-width: 1080px;
  --header-max-width: var(--content-max-width);
  --header-height: 64px;
  --header-height-mobile: 48px;
  --header-padding-desktop: clamp(24px, 4vw, 48px);
  --header-padding-mobile: 16px;
  
  /* Typography */
  --font-size-logo: 30px;
  --font-size-logo-mobile: 22px;
  --font-size-nav: 18px;
  --font-size-nav-mobile: 16px;
  
  /* Spacing */
  --spacing-nav: 28px;
  --spacing-nav-mobile: 12px;
  
  /* Border */
  --border-radius: 8px;
}

.main-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  font-family: 'Pretendard', 'Noto Sans KR', 'SUIT', 'Inter', sans-serif;
  transition: box-shadow 0.2s, background 0.2s;
  backdrop-filter: blur(4px);
  margin: 0;
  padding: 0;
}

.main-header.scrolled {
  background: rgba(255, 255, 255, 0.98);
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
  padding: 0 40px;
  min-height: 64px;
  gap: 32px;
  box-sizing: border-box;
}

.logo-link {
  text-decoration: none;
  color: inherit;
}

.logo {
  font-size: 30px;
  font-weight: 700;
  color: #6DB872;
  letter-spacing: 1.5px;
  user-select: none;
  margin-left: 0;
  font-family: inherit;
}

.mobile-nav-toggle {
  display: none;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  position: relative;
  z-index: 101;
}

.mobile-nav-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background-color: var(--text-primary);
  margin: 5px 0;
  transition: transform 0.3s, opacity 0.3s;
}

.mobile-nav-toggle[aria-expanded="true"] span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-nav-toggle[aria-expanded="true"] span:nth-child(2) {
  opacity: 0;
}

.mobile-nav-toggle[aria-expanded="true"] span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-nav);
}

nav a,
nav .router-link-active {
  text-decoration: none;
  color: #222;
  font-weight: 500;
  font-size: 18px;
  padding: 6px 10px;
  border-radius: 8px;
  transition: color 0.15s, background 0.15s;
  position: relative;
  font-family: inherit;
}

nav a:hover,
nav .router-link-active {
  background: #e0f7e9;
  color: #6DB872;
  font-weight: bold;
}

.header-btn {
  padding: 6px 18px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 18px;
  border: none;
  margin-left: 8px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.login-btn {
  background: #fff;
  color: #1BC47D;
  border: 2px solid #1BC47D;
}

.login-btn:hover {
  background: #e0f7e9;
}

.signup-btn {
  background: #1BC47D;
  color: #fff;
  border: 2px solid #1BC47D;
}

.signup-btn:hover {
  background: #6DB872;
  color: #fff;
}

.logout-btn {
  background: #fff;
  color: #1BC47D;
  border: 2px solid #1BC47D;
}

.logout-btn:hover {
  background: #e0f7e9;
}

.withdraw-btn {
  background: #1BC47D;
  color: #fff;
  border: 2px solid #1BC47D;
}

.withdraw-btn:hover {
  background: #6DB872;
  color: #fff;
}

@media (max-width: 700px) {
  .header-inner {
    padding-inline: var(--header-padding-mobile);
    min-height: var(--header-height-mobile);
  }

  .logo {
    font-size: var(--font-size-logo-mobile);
    margin-left: 0;
  }

  .header-left,
  .header-center,
  .header-right {
    flex: unset;
    justify-content: center;
  }

  .mobile-nav-toggle {
    display: block;
  }

  nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--header-bg);
    padding: 16px;
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-nav-mobile);
  }

  nav.mobile-nav-open {
    display: flex;
  }

  nav a,
  nav .router-link-active {
    width: 100%;
    text-align: center;
    font-size: var(--font-size-nav-mobile);
    padding: 12px;
  }
}
</style> 