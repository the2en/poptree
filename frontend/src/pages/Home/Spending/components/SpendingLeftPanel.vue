<template>
  
    <div class="summary-card bar-chart-card">
      <div class="summary-title">카테고리별 소비금액(막대그래프)</div>
      <apexchart
        type="bar"
        :options="barChartOptions"
        :series="barChartSeries"
        height="700px"
      />
    </div>
  
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ApexCharts from 'vue3-apexcharts'

const props = defineProps<{
  categorySummary: { category: string, amount: number }[]
}>()

const totalAmount = computed(() => (props.categorySummary ?? []).reduce((sum, c) => sum + c.amount, 0))
const barChartSeries = computed(() => [{
  name: '비율(%)',
  data: (props.categorySummary ?? []).map(c => totalAmount.value ? +(c.amount / totalAmount.value * 100).toFixed(1) : 0)
}])
const barChartOptions = computed(() => ({
  chart: { type: 'bar', toolbar: { show: false } },
  plotOptions: { bar: { horizontal: true, borderRadius: 6 } },
  dataLabels: {
    enabled: true,
    formatter: val => val + '%',
    style: { fontSize: '13px' }
  },
  xaxis: {
    categories: (props.categorySummary ?? []).map(c => c.category),
    labels: { style: { fontSize: '13px' } }
  },
  colors: ['#1bc47d'],
  grid: { show: false },
  tooltip: {
    enabled: true,
    y: { formatter: val => val + '%' }
  },
}))
</script>

<style scoped>

</style> 