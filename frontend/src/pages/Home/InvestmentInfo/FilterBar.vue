<template>
  <div class="filterbar-layout">
    <div></div>
    <div class="filterbar-inner">
      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat"
          :class="{ active: selectedCategory === cat }"
          @click="setCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>
      <div class="bank-list">
        <button
          v-for="bank in banks"
          :key="bank.name"
          :class="{ active: selectedBanks.includes(bank.name) }"
          @click="toggleBank(bank.name)"
          class="bank-card"
        >
          <img v-if="bank.icon" :src="bank.icon" :alt="bank.name" class="bank-icon" />
          <span class="bank-name">{{ bank.name }}</span>
          <span v-if="selectedBanks.includes(bank.name)" class="checkmark">✔</span>
        </button>
        <div class="settings-wrap">
          <button class="settings-button">
            <svg width="24" height="24" fill="none"><circle cx="12" cy="12" r="10" stroke="#1BC47D" stroke-width="2"/><rect x="10" y="7" width="4" height="10" rx="2" fill="#1BC47D"/></svg>
          </button>
          <span class="settings-badge">6</span>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  categories: { type: Array, default: () => ["예금", "적금"] },
  selectedCategory: { type: String, default: '예금' },
  selectedBanks: { type: Array, default: () => ["KB국민", "신한", "하나", "우리", "NH농협"] }
})
const emit = defineEmits(['update:selectedCategory', 'update:selectedBanks'])

const logoFiles = import.meta.glob('@/assets/bank.logo/*.svg', { eager: true, import: 'default' })
const bankDefs = [
  { name: 'KB국민', keywords: ['KB국민'], icon: logoFiles['/src/assets/bank.logo/KB_logo.svg'] },
  { name: '신한', keywords: ['신한'], icon: logoFiles['/src/assets/bank.logo/shinhan-bank.svg'] },
  { name: '하나', keywords: ['하나'], icon: logoFiles['/src/assets/bank.logo/Hana_Bank_Logo_(kor).svg'] },
  { name: '우리', keywords: ['우리'], icon: logoFiles['/src/assets/bank.logo/wooribank.svg'] },
  { name: 'NH농협', keywords: ['농협', 'NH'], icon: logoFiles['/src/assets/bank.logo/NH.svg'] },
]
const banks = bankDefs.map(b => ({ name: b.name, icon: b.icon }))

const selectedCategory = ref(props.selectedCategory)
const selectedBanks = ref([...props.selectedBanks])

function setCategory(cat: string) {
  selectedCategory.value = cat
  emit('update:selectedCategory', cat)
}

function toggleBank(bank: string) {
  if (selectedBanks.value.includes(bank)) {
    selectedBanks.value = selectedBanks.value.filter(b => b !== bank)
  } else {
    selectedBanks.value.push(bank)
  }
  emit('update:selectedBanks', selectedBanks.value)
}
</script>

<style scoped>
.filterbar-layout {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 40px;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
}

.filterbar-inner {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 16px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
  align-items: center;
}

.category-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  justify-content: center;
}

.category-tabs button {
  border: none;
  background: #f5f6fa;
  color: #888;
  font-size: 18px;
  font-weight: 500;
  border-radius: 20px;
  padding: 10px 28px;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: none;
}

.category-tabs button.active {
  background: #fff;
  color: #222;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.bank-list {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  justify-content: center;
}

.bank-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 92px;
  height: 92px;
  background: #fff;
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  font-size: 16px;
  color: #1a1a1a;
  font-weight: 500;
  position: relative;
  transition: border 0.15s, box-shadow 0.15s, background 0.15s;
  cursor: pointer;
  gap: 6px;
}

.bank-card.active {
  border: 2px solid #1BC47D;
  background: #f6fffa;
  color: #1BC47D;
  box-shadow: 0 2px 8px rgba(27,196,125,0.08);
}

.bank-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: contain;
  margin-bottom: 2px;
  background: #fff;
  display: block;
  border: 1px solid #eee;
}

.bank-name {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 2px;
}

.checkmark {
  color: #1BC47D;
  font-size: 18px;
  position: absolute;
  top: 8px;
  right: 8px;
}

.settings-wrap {
  position: relative;
  margin-left: 8px;
  display: flex;
  align-items: center;
}

.settings-button {
  width: 44px;
  height: 44px;
  border: none;
  background: #f5f6fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.settings-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #1BC47D;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #fff;
  box-shadow: 0 1px 4px rgba(27,196,125,0.12);
}

@media (max-width: 700px) {
  .filterbar-layout {
    grid-template-columns: 1fr;
    gap: 0;
    max-width: 100vw;
    padding: 0;
  }
  .filterbar-inner {
    width: 100%;
    padding: 12px 8px;
  }
}
</style> 