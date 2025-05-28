<template>
  <div class="etf-detail-root">
    <div class="etf-tab">
      <button :class="{active: tab==='korea'}" @click="tab='korea'">한국 ETF</button>
      <button :class="{active: tab==='us'}" @click="tab='us'">미국 ETF</button>
    </div>
    <div class="etf-header-row">
      <div class="etf-header-name">종목명</div>
      <div class="etf-header-symbol">종목코드</div>
      <div class="etf-header-price">지수</div>
      <div class="etf-header-date">갱신일</div>
    </div>
    <ul class="etf-list">
      <li v-for="item in filteredList" :key="item.symbol + item.record_date" class="etf-item">
        <div class="etf-name">{{ item.name }}</div>
        <div class="etf-symbol">{{ item.symbol }}</div>
        <div class="etf-price">{{ item.close_price != null ? Number(item.close_price).toLocaleString() : '-' }}</div>
        <div class="etf-date">{{ item.record_date }}</div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const tab = ref<'korea'|'us'>('korea')

// 쿼리스트링으로 전달된 marketData 파싱
const allData = ref<any[]>([])
try {
  allData.value = JSON.parse(route.query.data as string || '[]')
} catch { allData.value = [] }

// symbol별로 최신 날짜 데이터만 추출
const latestBySymbol = computed(() => {
  const map = new Map<string, any>()
  for (const item of allData.value) {
    const prev = map.get(item.symbol)
    if (!prev || prev.record_date < item.record_date) {
      map.set(item.symbol, item)
    }
  }
  return Array.from(map.values())
})

const filteredList = computed(() => {
  if (tab.value === 'korea') {
    return latestBySymbol.value.filter(item => item.symbol.includes('.KS'))
  } else {
    return latestBySymbol.value.filter(item => !item.symbol.includes('.KS'))
  }
})
</script>

<style scoped>
.etf-detail-root {
  max-width: 700px;
  margin: 40px auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 32px 24px;
}
.etf-tab {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}
.etf-tab button {
  background: #f5f5f5;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 1rem;
  cursor: pointer;
  color: #888;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
}
.etf-tab button.active {
  background: #e0f7e9;
  color: #1bc47d;
  font-weight: 700;
}
.etf-header-row {
  display: flex;
  font-weight: 700;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 2px;
  color: #1976d2;
  font-size: 1.05rem;
}
.etf-header-name { flex: 0.7; color: #222; min-width: 120px; text-align: left; }
.etf-header-symbol { min-width: 120px; color: #1bc47d; text-align: left; }
.etf-header-price { min-width: 80px; text-align: right; }
.etf-header-date { min-width: 90px; text-align: right; }
.etf-list {
  list-style: none;
  padding: 10px;
  margin: 0;
  max-height: 800px;
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE, Edge */
}
.etf-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}
.etf-item {
  display: flex;
  align-items: center;
  gap: 18px;
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 0;
  
}
.etf-symbol {
  font-weight: 700;
  color: #1bc47d;
  min-width: 120px;
  text-align: center;
}
.etf-name { flex: 0.7; color: #222; min-width: 120px; text-align: left; }
.etf-price {
  font-size: 1.05rem;
  color: #1976d2;
  min-width: 80px;
  text-align: right;
}
.etf-date {
  min-width: 90px;
  color: #888;
  font-size: 0.98rem;
  text-align: right;
}
</style> 