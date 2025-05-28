<template>
  <div>
    <section class="hero">
      <img src="/pop-tree.svg" alt="PopTree 로고" class="hero-tree-img" />
      <h1>나의 소비 습관을 키워보세요!</h1>
      <p>소비를 관리하고, 나무처럼 자산을 키우는 Pop Tree</p>
    </section>

    <section class="section">
      <div class="cards">
        <div class="card invest-card" @click="goToRanking">
          <h3>🏆 랭킹 정보</h3>
          <p>전체 랭킹에서 나의 위치를 확인하고 도전하세요.</p>
        </div>
        <div class="card invest-card" @click="goToSpending">
          <h3>💰 소비 지출 정보</h3>
          <p>나의 소비 지출 정보를 확인하고 관리하세요.</p>
        </div>
        <div class="card invest-card" @click="goToInvest">
          <h3>📈 투자정보</h3>
          <p>금융상품 정보를 비교하고 추천 금융 상품을 확인하세요.</p>
        </div>
        
      </div>
    </section>

    <footer>
      © 2025 Pop Tree. All rights reserved.
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'


const router = useRouter()
function goToInvest() {
  router.push('/invest')
}


function goToSpending() {
  router.push('/spending')
}

function goToRanking() {
  router.push('/ranking')
}
</script>
<style scoped>
body {
  margin: 0;
  font-family: 'Pretendard', sans-serif;
  background-color: #F7F9FA;
  color: #333;
}
.main-header {
  background-color: #ffffff;
  padding: 20px 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 28px;
  font-weight: bold;
  color: #6DB872;
}
nav {
  display: flex;
  align-items: center;
}
nav a, nav .router-link-active {
  margin-left: 20px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 18px;
}
nav .router-link-active {
  color: #6DB872;
  font-weight: bold;
}
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-top: 32px;
  margin-bottom: 32px;
  position: relative;
  background: linear-gradient(to bottom, #F0FFF4, #F7F9FA);
  width: 100%;
  padding: 60px 0 40px 0;
  border-radius: 0 0 32px 32px;
}
.hero-tree-img {
  width: 170px;
  height: 170px;
  object-fit: contain;
  border-radius: 50%;
  margin-bottom: 8px;
}
.hero h1 {
  font-size: 48px;
  margin-bottom: 16px;
  color: #333;
}
.hero p {
  font-size: 18px;
  color: #555;
}
.section {
  max-width: 1200px;
  margin: 60px auto;
  padding: 0 20px;
}
.cards {
  display: flex;
  justify-content: space-between;
  gap: 32px;
  max-width: 600px;
  margin: 0 auto;
}
.card {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
}
.card h3 {
  margin-bottom: 12px;
  color: #333;
}
.card p {
  color: #666;
}
footer {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 14px;
}
@media (max-width: 900px) {
  .cards {
    flex-direction: column;
    gap: 20px;
  }
  .hero h1 {
    font-size: 32px;
  }
}
@media (max-width: 600px) {
  .hero-tree-img {
    width: 110px;
    height: 110px;
  }
}
.invest-card {
  cursor: pointer;
  border: 2px solid #6DB872;
}
.invest-card:hover {
  box-shadow: 0 8px 32px rgba(109,184,114,0.15);
  border-color: #1BC47D;
}
</style> 