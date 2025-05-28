<template>
  <div class="stat-card">
    <div class="stat-title">카테고리별 비중</div>
    <apexchart
      type="donut"
      :options="chartOptions"
      :series="series"
      :highlighted-index="hoverIndex"
      @dataPointMouseEnter="onChartHover"
      @dataPointMouseLeave="onChartLeave"
    />
    <ul class="category-list">
      <li
        v-for="(cat, i) in displayCategories"
        :key="cat.category"
        class="category-item"
        :class="{ active: hoverIndex === i }"
        @mouseenter="hoverIndex = i"
        @mouseleave="hoverIndex = null"
        @click="onCategoryClick(i)"
      >
        <span class="cat-color" :style="{ background: cat.color }"></span>
        <span class="cat-name">{{ cat.category }}</span>
        <span class="cat-ratio">{{ cat.ratio.toFixed(1) }}%</span>
        <span class="cat-amount">{{ cat.amount.toLocaleString() }}원</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ApexCharts from 'vue3-apexcharts'

const props = defineProps<{ categorySummary: { category: string, amount: number }[] }>()

const colors = [
  '#1bc47d', '#ff7a00', '#1b6dc4', '#e23c3c', '#f7c325', '#a259ec', '#f24e1e', '#2d9cdb', '#27ae60', '#eb5757'
]
const sorted = computed(() =>
  [...props.categorySummary].sort((a, b) => b.amount - a.amount)
)
const top9 = computed(() => sorted.value.slice(0, 9))
const etcAmount = computed(() =>
  sorted.value.slice(9).reduce((sum, c) => sum + c.amount, 0)
)
const displayCategories = computed(() => {
  const arr = top9.value.map((c, i) => ({
    ...c,
    color: colors[i % colors.length]
  }))
  if (etcAmount.value > 0) {
    arr.push({
      category: '기타',
      amount: etcAmount.value,
      color: colors[9],
    })
  }
  const total = arr.reduce((sum, c) => sum + c.amount, 0)
  return arr.map(c => ({
    ...c,
    ratio: total ? (c.amount / total) * 100 : 0
  }))
})
const series = computed(() => displayCategories.value.map(c => c.amount))

const hoverIndex = ref<number|null>(null)

function onChartHover(event, chartContext, config) {
  hoverIndex.value = config.dataPointIndex
}
function onChartLeave() {
  hoverIndex.value = null
}
function onCategoryClick(i) {
  
}

const chartOptions = computed(() => ({
  labels: displayCategories.value.map(c => c.category),
  legend: { show: false },
  dataLabels: { enabled: true },
  chart: {
    toolbar: { show: false },
    events: {
      dataPointMouseEnter: onChartHover,
      dataPointMouseLeave: onChartLeave,
    },
  },
  colors: displayCategories.value.map(c => c.color),
  states: {
    normal: { filter: { type: 'none' } },
    hover: { filter: { type: 'lighten', value: 0.2 } },
    active: { filter: { type: 'darken', value: 0.3 } },
  },
  tooltip: { enabled: true },
  plotOptions: {
    pie: {
      donut: { labels: { show: false } },
      expandOnClick: false,
    },
  },
  highlight: {
    series: hoverIndex.value !== null ? [hoverIndex.value] : [],
  },
}))
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  padding: 24px 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  align-items: center;
}
.stat-title {
  font-size: 18px;
  font-weight: 700;
  margin: 8px 0 12px 0;
}
.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  margin-top: 10px;
  max-height: 260px;
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
}
.category-list::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
.category-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  padding: 4px 0;
  cursor: pointer;
  transition: background 0.15s;
}
.category-item.active, .category-item:hover {
  background: #f7f7f7;
}
.cat-color {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 4px;
}
.cat-name {
  flex: 1;
  font-weight: 500;
  color: #333;
}
.cat-ratio {
  color: #1bc47d;
  font-weight: 600;
  margin-right: 8px;
}
.cat-amount {
  color: #888;
  font-size: 14px;
}
</style> 