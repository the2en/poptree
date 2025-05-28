<template>
  <div class="rate-card-group">
    <div v-if="loading">로딩 중...</div>
    <div v-else-if="error">{{ error }}</div>
    <template v-else>
      <!-- USD 환율 카드 -->
      <div class="rate-card">
        <div class="rate-title">
          <img class="flag" src="https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg" alt="US Flag" />
          USD 현재 환율
        </div>
        <div class="rate-value">
          {{ usdRate.value }} <span class="unit">원</span>
        </div>
        <div class="rate-diff up">전일 대비 ▲ {{ usdRate.diff }}</div>
        <div class="rate-chart">
          <!-- 임시 차트 -->
          <svg width="100%" height="40" viewBox="0 0 120 40">
            <polyline fill="#e0f7e9" stroke="#1bc47d" stroke-width="2" points="0,35 30,30 60,10 90,5 120,20" />
            <circle cx="0" cy="35" r="2" fill="#1bc47d" />
            <circle cx="30" cy="30" r="2" fill="#1bc47d" />
            <circle cx="60" cy="10" r="2" fill="#1bc47d" />
            <circle cx="90" cy="5" r="2" fill="#1bc47d" />
            <circle cx="120" cy="20" r="2" fill="#1bc47d" />
          </svg>
        </div>
        <div class="rate-x-labels">
          <span>1월</span><span>2월</span><span>4월</span><span>5월</span>
        </div>
      </div>
      <!-- 미국 기준금리 카드 -->
      <div class="rate-card">
        <div class="rate-title">
          <img class="flag" src="https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg" alt="US Flag" />
          미국 기준금리
        </div>
        <div class="rate-value">
          {{ usBaseRate.value }} <span class="unit">%</span>
        </div>
      </div>
      <!-- 한국 기준금리 카드 -->
      <div class="rate-card">
        <div class="rate-title">
          <img class="flag" src="https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg" alt="Korea Flag" />
          한국 기준금리
        </div>
        <div class="rate-value">
          {{ krBaseRate.value }} <span class="unit">%</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'

const usdRate = ref({ value: '', diff: '' })
const usBaseRate = ref({ value: ''})
const krBaseRate = ref({ value: ''})
const loading = ref(true)
const error = ref('')

async function fetchRates() {
  try {
    loading.value = true
    // 환율
    const usdRes = await axios.get(`${API_BASE_URL}/api/investments/exchange-rate/usd/`)
    const usdList = usdRes.data
    if (usdList.length > 1) {
      const last = usdList[usdList.length - 1]
      const prev = usdList[usdList.length - 2]
      usdRate.value = {
        value: last.value.toFixed(2),
        diff: (last.value - prev.value).toFixed(2)
      }
    } else if (usdList.length === 1) {
      usdRate.value = { value: usdList[0].value.toFixed(2), diff: '0.00' }
    } else {
      usdRate.value = { value: '-', diff: '-' }
    }
    // 미국 기준금리
    const usRes = await axios.get(`${API_BASE_URL}/api/investments/us-base-rate/`)
    usBaseRate.value = { value: String(usRes.data.value)}
    console.log(usBaseRate.value)
    // 한국 기준금리
    const krRes = await axios.get(`${API_BASE_URL}/api/investments/kr-base-rate/`)
    krBaseRate.value = { value: String(krRes.data.value) }
    console.log(krBaseRate.value)
  } catch (e) {
    error.value = '데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRates()
})
</script>

<style scoped>
.rate-card-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #fffbe9;
  border-radius: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 20px 12px;
  /* min-width: 340px; */
  max-width: 320px;
}
.rate-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
  padding: 14px 10px 10px 10px;
  margin-bottom: 6px;
}
.rate-title {
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.flag {
  width: 22px;
  height: 16px;
  border-radius: 4px;
  object-fit: cover;
  background: #eee;
  display: inline-block;
}
.rate-value {
  font-size: 24px;
  font-weight: 700;
  color: #ff7a00;
  margin-bottom: 2px;
}
.rate-value .unit {
  font-size: 14px;
  font-weight: 400;
  margin-left: 2px;
}
.rate-diff {
  font-size: 12px;
  color: #1bc47d;
  margin-bottom: 4px;
}
.rate-diff.up {
  color: #1bc47d;
}
.rate-chart {
  height: 28px;
  background: none;
  border-radius: 8px;
  margin-top: 2px;
}
.rate-x-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: #888;
  margin-top: 1px;
}
</style> 