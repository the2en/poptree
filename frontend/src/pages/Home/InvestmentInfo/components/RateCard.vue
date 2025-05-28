<template>
  <div class="rate-card">
    <div class="rate-title">
      <span v-if="showFlag" class="flag" :style="{ backgroundImage: `url(${flagUrl})` }" />
      {{ title }}
    </div>
    <div class="rate-value">{{ value }}<span class="unit">{{ unit }}</span></div>
    <div :class="['rate-diff', { up: isUp }]">{{ diffText }}</div>
    <div v-if="showChart" class="rate-chart" :style="{ background: chartBackground }"></div>
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
interface Props {
  title: string;
  value: string | number;
  unit: string;
  diff: number;
  diffUnit?: string;
  isUp: boolean;
  showFlag?: boolean;
  flagUrl?: string;
  showChart?: boolean;
  chartColor?: string;
}
const props = withDefaults(defineProps<Props>(), {
  diffUnit: '',
  showFlag: false,
  flagUrl: '',
  showChart: true,
  chartColor: '#e0f7e9',
});
const diffText = computed(() => {
  const prefix = props.isUp ? '▲' : '▼';
  return `전일 대비 ${prefix} ${Math.abs(props.diff)}${props.diffUnit || props.unit}`;
});
const chartBackground = computed(() => {
  return `linear-gradient(90deg, ${props.chartColor} 0%, #fff 100%)`;
});
</script> 