import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/Home/HomePage.vue'
import LoginPage from '../pages/Home/Login/LoginPage.vue'
import SignUpPage from '../pages/Home/Login/SignUp/SignUpPage.vue'
import MyDataConsentPage from '../pages/Home/Login/MyDataConsent/MyDataConsentPage.vue'
import InvestmentInfoPage from '../pages/Home/InvestmentInfo/InvestmentInfoPage.vue'
import SpendingPage from '../pages/Home/Spending/SpendingPage.vue'
import RankingPage from '../pages/Home/RankingPage.vue'
import EtfDetailPage from '../pages/Home/InvestmentInfo/EtfDetailPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignUpPage },
  { path: '/mydata-consent', component: MyDataConsentPage },
  { path: '/invest', component: InvestmentInfoPage },
  { path: '/spending', component: SpendingPage },
  { path: '/ranking', component: RankingPage },
  { path: '/etf-detail', component: EtfDetailPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Pinia store import 및 라우터 가드 추가
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

router.beforeEach((to, from, next) => {
  // Pinia store는 setup 밖에서 직접 호출 시 인스턴스가 없을 수 있으므로, window.__pinia__에서 가져옴
  let auth
  try {
    auth = useAuthStore()
  } catch (e) {
    // SSR 등에서 Pinia 인스턴스가 없을 때 예외 방지
    return next()
  }
  if ((to.path === '/login' || to.path === '/signup') && auth.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router 