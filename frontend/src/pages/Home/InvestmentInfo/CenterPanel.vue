<template>
  <main class="center-panel">
    <div class="product-list-header">
      <div class="count">{{ productCount }}개</div>
      <div class="filters">
        <span class="filter">전체</span>
        <span class="sort">정렬</span>
      </div>
    </div>
    <ul class="product-list">
      <li v-for="product in products" :key="product.id" class="product-item">
        <img :src="bankLogoByName(product.kor_co_nm)" :alt="product.kor_co_nm" class="bank-logo">
        <div class="product-info">
          <h3 class="product-title">{{ product.fin_prdt_nm }}</h3>
          <p class="product-bank">{{ product.kor_co_nm }}</p>
          <div class="product-tags">
            <span class="tag">{{ product.type }}</span>
          </div>
        </div>
        <div class="product-rate">
          <div class="rate-max">{{ product.highest_rate }}%</div>
          <div class="rate-base">기본 {{ product.lowest_rate }}%</div>
        </div>
      </li>
    </ul>
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useInvestmentStore } from '@/stores/investment'

interface Product {
  id: number
  fin_prdt_cd: string
  fin_co_no: string
  kor_co_nm: string
  fin_prdt_nm: string
  type: string
  join_way: string
  join_deny: string
  join_member: string
  spcl_cnd: string
  etc_note: string
  mtrt_int: string
  intr_rate_type_nm: string | null
  max_limit: number | null
  interest_detail: {
    [key: string]: {
      intr_rate: number
      intr_rate2: number
    }
  }
  lowest_rate: number
  highest_rate: number
  dcls_month: string
  dcls_strt_day: string
  dcls_end_day: string | null
  fin_co_subm_day: string
  record_date: string
  bank_logo?: string
}

const investmentStore = useInvestmentStore()
const props = defineProps<{
  products: Product[]
}>()

const productCount = computed(() => props.products?.length || 0)

const logoFiles = import.meta.glob('@/assets/bank.logo/*.svg', { eager: true, import: 'default' })
const bankLogoByName = (name: string) => {
  if (!name) return null;
  if (name.includes('신한')) return logoFiles['/src/assets/bank.logo/shinhan-bank.svg'];
  if (name.includes('KB') || name.includes('국민')) return logoFiles['/src/assets/bank.logo/KB_logo.svg'];
  if (name.includes('하나')) return logoFiles['/src/assets/bank.logo/Hana_Bank_Logo_(kor).svg'];
  if (name.includes('우리')) return logoFiles['/src/assets/bank.logo/wooribank.svg'];
  if (name.includes('농협') || name.includes('NH')) return logoFiles['/src/assets/bank.logo/NH.svg'];
  return null;
}
</script>

<style scoped>
.center-panel {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 18px 10px;
  /* min-width: 520px; */
  max-width: 600px;
}

.product-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.count {
  color: #1bc47d;
  font-weight: 700;
  font-size: 16px;
}

.filters {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #888;
  font-size: 12px;
}

.filter {
  font-weight: 500;
  cursor: pointer;
}

.sort {
  font-weight: 500;
  cursor: pointer;
}

.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 320px;
  overflow-y: auto;
  /* 스크롤바 숨기기 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE, Edge */
}
.product-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}

.product-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  padding: 10px 0;
  gap: 10px;
}

.bank-logo {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: contain;
  background: #fff;
  display: inline-block;
  border: 1px solid #eee;
}

.product-info {
  flex: 1;
}

.product-title {
  font-size: 14px;
  font-weight: 700;
}

.product-bank {
  font-size: 11px;
  color: #888;
  margin-bottom: 2px;
}

.product-tags {
  display: flex;
  gap: 4px;
}

.tag {
  background: #f5f5f5;
  color: #888;
  font-size: 10px;
  border-radius: 8px;
  padding: 1px 6px;
}

.product-rate {
  min-width: 60px;
  text-align: right;
}

.rate-max {
  color: #1bc47d;
  font-weight: 700;
  font-size: 12px;
}

.rate-base {
  color: #888;
  font-size: 10px;
}
</style> 