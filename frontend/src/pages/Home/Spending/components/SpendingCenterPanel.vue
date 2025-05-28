<template>
  <main class="center-panel">
    <div class="calendar-wrap">
    <vue-cal
      :selected-date="selectedDate"
      :events="calendarEvents"
      :disable-views="['years', 'year', 'week', 'day', 'agenda']"
      default-view="month"
      hide-view-selector
      locale="ko"
      start-week-on-sunday

    />
    </div>
    <div class="daily-list-wrap">
    <ul class="daily-list">
      <li v-for="item in daily" :key="item.date" class="daily-item">
        <div class="date">{{ item.date }}</div>
        <div class="amount">{{ item.total_spending.toLocaleString() }} 원</div>
        <div class="categories">
          <span
            v-for="cat in item.categories"
            :key="cat.category"
            class="cat"
          >{{ cat.category }}: {{ cat.amount.toLocaleString() }}</span>
        </div>
      </li>
    </ul>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

const props = defineProps<{ daily: any[], year: number, month: number }>()
const selectedDate = ref(null)

// daily 데이터를 vue-cal 이벤트로 변환
const calendarEvents = computed(() =>
  props.daily.map(item => ({
    start: item.date,
    end: item.date,
    title: item.total_spending.toLocaleString() + '원',
    content: item.categories.map(cat => `${cat.category}: ${cat.amount.toLocaleString()}`).join(', ')
  }))
)

</script>

<style scoped>
.center-panel {
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 60px;
}

:deep(.vuecal__weekdays-headings) {
  font-size: 15px;
  font-weight: 700;
  color: #222;
  background: #f7f7f7;
  border-radius: 8px 8px 0 0;
  letter-spacing: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cell-date {
  font-size: 15px;
  font-weight: 600;
  color: #222;
  text-align: center;
}
.cell-amount {
  font-size: 13px;
  color: #ff7a00;
  margin-top: 2px;
  text-align: center;
}
.week-total {
  font-size: 13px;
  color: #1bc47d;
  margin-top: 4px;
  font-weight: 700;
  text-align: center;
}
.daily-list-header {
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
.daily-list {
  list-style: none;
  padding: 0;
  margin-top: 0px;
  max-height: 320px;
  overflow-y: auto;
}
.daily-item {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #f0f0f0;
  padding: 10px 0;
  gap: 4px;
}
.date { color: #888; font-size: 14px; }
.amount { font-weight: 700; color: #ff7a00; }
.categories { display: flex; flex-wrap: wrap; gap: 8px; font-size: 13px; }
.cat { color: #1bc47d; }
</style> 