<template>
  <div class="spending-root">
   
    <!-- 바디 -->
    <div class="body">
      <!-- 왼쪽 사이드바 -->
      <aside class="sidebar-left  ">
        <SpendingLeftPanel
          v-if="statistics && typeof statistics.total_spending === 'number' && Array.isArray(statistics.category_summary)"
          :total="statistics.total_spending"
          :categorySummary="statistics.category_summary"
        />
      </aside>

      <!-- 인바디(메인) -->
      <main class="inbody">
        <SpendingCenterPanel v-if="statistics && Array.isArray(statistics.daily) && typeof statistics.year === 'number' && typeof statistics.month === 'number'" :daily="statistics.daily" :year="statistics.year" :month="statistics.month" />
      </main>

      <!-- 오른쪽 사이드바 -->
      <aside class="sidebar sidebar-right">
        <SpendingRightPanel v-if="statistics && Array.isArray(statistics.category_summary)" :categorySummary="statistics.category_summary" />
      </aside>
    </div>

    <!-- 푸터 -->
    <footer class="footer">
      <div class="footer-ai-annonce"></div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'
import SpendingLeftPanel from './components/SpendingLeftPanel.vue'
import SpendingCenterPanel from './components/SpendingCenterPanel.vue'
import SpendingRightPanel from './components/SpendingRightPanel.vue'


const statistics = ref<any>(null)

onMounted(async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/api/spending/statistics/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (res.status === 401) {
      window.location.href = '/login'
      return
    }
    statistics.value = res.data
  } catch (e) {
    console.error('spending statistics fetch error:', e)
  }
})
</script>

<style scoped>
.spending-root {
  width: 100%;
  max-width: 1200px;
  margin: 32px auto 0 auto;
  padding: 0;
  box-sizing: border-box;
  background: #fff;
}
.header {
  position: absolute;
  width: 1920px;
  height: 80px;
  left: 0;
  top: 0;
  background: #fff;
}
.body {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 2.2fr) minmax(0, 1.1fr);
  gap: 20px;
  padding: 28px 0;
  box-sizing: border-box;
  background: none;
}
.sidebar-left, .inbody, .sidebar-right {
  padding: 0;
  min-width: 0;
}
.sidebar-left {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.inbody {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 32px 24px;
  min-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}
.sidebar-right {
  display: flex;
  justify-content: flex-start;
}
.footer {
  width: 100%;
  height: 100px;
  background: #fff;
  margin-top: 24px;
}
.footer-ai-annonce {
  width: 986px;
  height: 71px;
  margin: 0 auto;
}
@media (max-width: 900px) {
  .body {
    grid-template-columns: 1fr;
    gap: 10px;
    max-width: 100vw;
    padding: 0;
    border-radius: 12px;
  }
  .inbody {
    min-width: 0;
    padding: 16px 4px;
  }
}
</style> 