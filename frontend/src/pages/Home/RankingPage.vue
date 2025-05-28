<template>
  <div class="ranking-root">
    <div v-if="loading" class="loading">로딩 중...</div>
    <template v-else>
      <section class="my-ranking-section" v-if="myRanking">
        <h2>내 랭킹</h2>
        <div class="my-ranking-card">
          <span class="icon">👑</span>
          <div class="info">
            <div class="username">{{ myRanking.username }}</div>
            <div class="rank-score">
              <span class="rank">{{ myRanking.rank }}위</span>
              <span class="score">점수: {{ myRanking.score }}</span>
              <span class="rank-diff" :class="{ up: myRanking.rank_diff > 0, down: myRanking.rank_diff < 0 }">
                ({{ myRanking.rank_diff > 0 ? '▲' : myRanking.rank_diff < 0 ? '▼' : '-' }}{{ Math.abs(myRanking.rank_diff) }})
              </span>
            </div>
          </div>
        </div>
      </section>
      <section class="ranking-list-section">
        <h2>전체 랭킹 TOP 10</h2>
        <table class="ranking-table">
          <thead>
            <tr>
              <th>순위</th>
              <th>닉네임</th>
              <th>점수</th>
              <th>변화</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in rankingList" :key="item.username" :class="{ me: item.username === myRanking?.username }">
              <td>
                <span v-if="item.rank === 1">🥇</span>
                <span v-else-if="item.rank === 2">🥈</span>
                <span v-else-if="item.rank === 3">🥉</span>
                <span v-else>{{ item.rank }}</span>
              </td>
              <td>{{ item.username }}</td>
              <td>{{ item.score }}</td>
              <td :class="{ up: item.rank_diff > 0, down: item.rank_diff < 0 }">
                {{ item.rank_diff > 0 ? '▲' : item.rank_diff < 0 ? '▼' : '-' }}{{ Math.abs(item.rank_diff) }}
              </td>
            </tr>
          </tbody>
        </table>
      </section>
      <section class="history-section">
        <h2>내 랭킹 변화 <span class="period">(최근 7일)</span></h2>
        <div class="chart-desc">
          그래프는 최근 7일간의 내 순위 변화를 보여줍니다.<br>
          <b>1위에 가까울수록 그래프가 위로 올라갑니다.</b>
        </div>
        <apexchart type="line" :options="chartOptions" :series="chartSeries" height="260" v-if="history.length"/>
        <div v-else class="no-history">랭킹 변화 데이터가 없습니다.</div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import ApexCharts from 'vue3-apexcharts'
import axios from 'axios'
import { API_BASE_URL } from '@/api/base'

const loading = ref(true)
const myRanking = ref<any>(null)
const rankingList = ref<any[]>([])
const history = ref<any[]>([])

async function fetchRanking() {
  loading.value = true
  const res = await axios.get(`${API_BASE_URL}/api/ranking/today/`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } })
  const data = res.data
  myRanking.value = data.my_ranking
  rankingList.value = data.ranking_list
  loading.value = false
}
async function fetchHistory() {
  const res = await axios.get(`${API_BASE_URL}/api/ranking/history/`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } })
  const data = res.data
  history.value = data.history
}
onMounted(async () => {
  await fetchRanking()
  await fetchHistory()
})
const chartOptions = computed(() => ({
  chart: { toolbar: { show: false } },
  xaxis: {
    categories: history.value.map(h => h.date),
    title: { text: '날짜' }
  },
  yaxis: {
    reversed: true
  },
  stroke: { curve: 'smooth' },
  tooltip: { enabled: true },
}))
const chartSeries = computed(() => [{
  name: '순위',
  data: history.value.map(h => h.rank)
}])
</script>

<style scoped>
.ranking-root {
  max-width: 800px;
  margin: 40px auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 32px 24px;
}
.loading {
  text-align: center;
  font-size: 20px;
  color: #888;
}
.my-ranking-section {
  margin-bottom: 32px;
}
.my-ranking-card {
  display: flex;
  align-items: center;
  background: #f7fbe9;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 20px 24px;
  margin-top: 8px;
  gap: 18px;
}
.my-ranking-card .icon {
  font-size: 2.2rem;
  margin-right: 12px;
}
.my-ranking-card .info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.my-ranking-card .rank-score {
  display: flex;
  gap: 16px;
  align-items: center;
}
.my-ranking-card .rank-diff.up { color: #e23c3c; }
.my-ranking-card .rank-diff.down { color: #1b6dc4; }
.ranking-list-section {
  margin-bottom: 32px;
}
.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 8px;
}
.ranking-table th {
  background: #f0f4f8;
  font-weight: 700;
}
.ranking-table th, .ranking-table td {
  padding: 10px 6px;
  text-align: center;
  border-bottom: 1px solid #eee;
}
.ranking-table tr.me {
  background: #e0f7e9;
  font-weight: 700;
}
.ranking-table td.up { color: #e23c3c; }
.ranking-table td.down { color: #1b6dc4; }
.period {
  font-size: 0.95rem;
  color: #888;
  margin-left: 8px;
}
.no-history {
  text-align: center;
  color: #aaa;
  margin: 32px 0;
}
.history-section {
  margin-top: 32px;
}
.chart-desc {
  font-size: 0.98rem;
  color: #666;
  margin-bottom: 10px;
  text-align: left;
  line-height: 1.5;
}
</style> 