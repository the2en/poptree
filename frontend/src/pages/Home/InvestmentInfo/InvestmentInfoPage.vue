<template>
  <div class="info-page">
    <FilterBar
      :categories="categories"
      v-model:selectedCategory="selectedCategory"
      v-model:selectedBanks="selectedBanks"
    />
    <div class="info-layout">
      <LeftPanel :exchangeRate="exchangeRate" :baseRate="baseRate" />
      <CenterPanel :products="filteredProducts" />
      <RightPanel :marketData="marketData" />
    </div>
    <AiRecommendButton :userId="userId" :userName="userName" :disabled="!userId" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useInvestmentStore } from '@/stores/investment'
import { useAuthStore } from '@/stores/auth'
import FilterBar from './FilterBar.vue'
import LeftPanel from './LeftPanel.vue'
import CenterPanel from './CenterPanel.vue'
import RightPanel from './RightPanel.vue'
import AiRecommendButton from './components/AiRecommendButton.vue'

const investmentStore = useInvestmentStore()
const auth = useAuthStore()

const products = ref([])
const marketData = ref([])
const loading = ref(false)
const error = ref(null)

// 카테고리/은행 상태를 상위에서 관리
const categories = ['예금', '적금']
const selectedCategory = ref(categories[0])
const allBankNames = ['KB국민', '신한', '하나', '우리', 'NH농협']
const selectedBanks = ref([...allBankNames])

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const productsResponse = await investmentStore.fetchProducts()
    products.value = productsResponse || []
    const marketResponse = await investmentStore.fetchMarketData()
    marketData.value = marketResponse || []
  } catch (error) {
    error.value = error.message
    products.value = []
    marketData.value = []
  } finally {
    loading.value = false
  }
})

// 카테고리+은행 필터링된 상품
const filteredProducts = computed(() => {
  return products.value.filter(p =>
    p.type === selectedCategory.value &&
    selectedBanks.value.some(bank => p.kor_co_nm && bank && p.kor_co_nm.includes(bank))
  )
})

// 임시 데이터 예시
const exchangeRate = {
  title: 'USD 현재 환율',
  value: '1,345.50',
  unit: '원',
  diff: 5.20,
  isUp: true,
  showFlag: true,
  flagUrl: 'https://via.placeholder.com/28x20',
  showChart: true,
  chartColor: '#e0f7e9',
};

const baseRate = {
  title: '한국 기준금리',
  value: '3.50',
  unit: '%',
  diff: -0.25,
  isUp: false,
  showFlag: false,
  showChart: true,
  chartColor: '#e0f7e9',
};

const productCount = computed(() => products.value.length)

const userId = computed(() => auth.user?.id)
const userName = computed(() => auth.user?.name)
</script>

<style scoped>
.info-page {
  width: 100%;
  max-width: 1100px;
  margin: 32px auto 0 auto;
  padding: 0;
  box-sizing: border-box;
  background: #fff;
}
.info-layout {
  display: grid;
  grid-template-columns: 1fr 2.2fr 1.1fr;
  gap: 20px;
  padding: 28px 0;
  box-sizing: border-box;
  background: none;
}
.left-panel, .center-panel, .right-panel {
  padding: 0;
  min-width: 0;
}
.left-panel {
  display: flex;
  justify-content: flex-end;
}
.rate-card-group {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: #fffbe9;
  border-radius: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 32px 24px;
  min-width: 240px;
}
.rate-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  border: 1px solid #f0f0f0;
  padding: 20px 18px 16px 18px;
  margin-bottom: 8px;
}
.rate-title {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.flag {
  width: 28px;
  height: 20px;
  border-radius: 4px;
  object-fit: cover;
  background: #eee;
  display: inline-block;
}
.rate-value {
  font-size: 32px;
  font-weight: 700;
  color: #ff7a00;
  margin-bottom: 4px;
}
.rate-value .unit {
  font-size: 18px;
  font-weight: 400;
  margin-left: 2px;
}
.rate-diff {
  font-size: 14px;
  color: #888;
  margin-bottom: 8px;
}
.rate-diff.up {
  color: #1bc47d;
}
.rate-chart {
  height: 40px;
  background: linear-gradient(90deg, #e0f7e9 0%, #fff 100%);
  border-radius: 8px;
  margin-top: 4px;
}
.center-panel {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 32px 24px;
  min-width: 480px;
}
.product-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.count {
  color: #1bc47d;
  font-weight: 700;
  font-size: 20px;
}
.filters {
  display: flex;
  align-items: center;
  gap: 18px;
  color: #888;
  font-size: 15px;
}
.filter.n-pay {
  font-weight: 600;
  color: #222;
}
.sort {
  font-weight: 500;
  cursor: pointer;
}
.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.product-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  padding: 18px 0;
  gap: 18px;
}
.bank-logo {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  background: #f5f5f5;
  display: inline-block;
}
.product-info {
  flex: 1;
}
.product-title {
  font-size: 18px;
  font-weight: 700;
}
.product-bank {
  font-size: 14px;
  color: #888;
  margin-bottom: 4px;
}
.product-tags {
  display: flex;
  gap: 6px;
}
.tag {
  background: #f5f5f5;
  color: #888;
  font-size: 12px;
  border-radius: 8px;
  padding: 2px 8px;
}
.product-rate {
  min-width: 90px;
  text-align: right;
}
.rate-max {
  color: #1bc47d;
  font-weight: 700;
  font-size: 16px;
}
.rate-base {
  color: #888;
  font-size: 13px;
}
.right-panel {
  display: flex;
  justify-content: flex-start;
}
.market-card {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 24px 18px;
  min-width: 240px;
  min-height: 328px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.market-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.market-row.blue .market-title,
.market-row.blue .market-value {
  color: #1a4ca0;
}
.market-row.red .market-title,
.market-row.red .market-value {
  color: #e23c3c;
}
.market-title {
  font-size: 15px;
  font-weight: 600;
}
.market-value {
  font-size: 15px;
  font-weight: 700;
}
.market-diff {
  font-size: 13px;
  font-weight: 400;
  margin-left: 4px;
}
.market-diff.up {
  color: #e23c3c;
}
.mini-chart {
  width: 36px;
  height: 28px;
  background: #e0eaff;
  border-radius: 6px;
}
@media (max-width: 900px) {
  .info-layout {
    grid-template-columns: 1fr;
    gap: 10px;
    max-width: 100vw;
    padding: 0;
    border-radius: 12px;
  }
}
</style>

<style>
body {
  background: #ffffff;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}
</style> 