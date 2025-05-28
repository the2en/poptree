<template>
  <div class="market-card">
    <button class="more-btn" @click="goToEtfDetail">ETF/지수 더보기</button>
    <div
      v-for="item in latestMarketData"
      :key="item.symbol"
      class="market-row"
    >
      <div class="mini-icon">
        <span v-if="item.change > 0" class="up">▲</span>
        <span v-else-if="item.change < 0" class="down">▼</span>
        <span v-else class="flat">-</span>
      </div>
      <div class="market-info">
        <div class="market-title">{{ item.displayName }}</div>
        <div class="market-value-row">
          <span
            class="market-value"
            :class="item.change > 0 ? 'red' : item.change < 0 ? 'blue' : ''"
          >
            {{ item.close_price != null ? Number(item.close_price).toLocaleString() : '-' }}
          </span>
          <span
            class="market-diff"
            :class="item.change > 0 ? 'red' : item.change < 0 ? 'blue' : ''"
          >
            <span v-if="item.change > 0">+{{ item.change }}</span>
            <span v-else-if="item.change < 0">{{ item.change }}</span>
            <span v-else>0</span>
            <span v-if="item.change !== 0"> ({{ item.daily_change_pct }}%)</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ marketData: any[] }>()
const router = useRouter()

// symbol별로 최신/전일 데이터 추출 및 변동값 계산
type MarketItem = { close_price: number, daily_change_pct: number|null, symbol: string, record_date: string }
const allowedSymbols = [
  '069500.KS', // 코스피
  '229200.KS', // 코스닥
  'SPY',       // S&P 500
  'QQQ',       // QQQ
  '458730.KS', // 배당주
  '411060.KS', // 금ETF
]
const symbolNameMap = {
  '069500.KS': '코스피',
  '229200.KS': '코스닥',
  'SPY': 'S&P 500',
  'QQQ': 'QQQ',
  '458730.KS': '배당주',
  '411060.KS': '금ETF',
}
const latestMarketData = computed(() => {
  if (!props.marketData.length) return []
  const grouped = props.marketData.reduce((acc, cur) => {
    if (!acc[cur.symbol]) acc[cur.symbol] = []
    acc[cur.symbol].push(cur)
    return acc
  }, {} as Record<string, any[]>)
  // allowedSymbols 순서대로 정렬 및 이름 매핑
  return allowedSymbols.map(symbol => {
    const list = grouped[symbol]
    if (!list) return null
    const sorted = list.sort((a, b) => b.record_date.localeCompare(a.record_date))
    const today = sorted[0]
    const prev = sorted[1]
    const change = prev ? +(today.close_price - prev.close_price).toFixed(2) : 0
    return {
      ...today,
      change,
      displayName: symbolNameMap[symbol]
    }
  }).filter(Boolean)
})

function goToEtfDetail() {
  router.push({
    path: '/etf-detail',
    query: { data: JSON.stringify(props.marketData) }
  })
}
</script>

<style scoped>
.market-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 14px 8px;
  /* min-width: 279px; min-height: 328px; */
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.more-btn {
  display: block;
  margin: 10px auto;
  background: #e0f7e9;
  color: #1bc47d;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.more-btn:hover {
  background: #c6f2d8;
}
.market-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}
.mini-icon {
  width: 28px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  border-radius: 6px;
}
.mini-icon .up { color: #e23c3c; }
.mini-icon .down { color: #1a4ca0; }
.mini-icon .flat { color: #888; }
.market-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.market-title {
  font-size: 10px;
  font-weight: 600;
  color: #888;
  margin-bottom: 1px;
}
.market-value-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
}
.market-value {
  font-size: 14px;
  font-weight: 700;
}
.market-diff {
  font-size: 11px;
  font-weight: 500;
  margin-left: 2px;
}
.red { color: #e23c3c !important; }
.blue { color: #1a4ca0 !important; }
.product-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 420px;
  overflow-y: auto;
  /* 스크롤바 숨기기 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE, Edge */
}
.product-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}
</style> 