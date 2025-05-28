import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'
import VueApexCharts from 'vue3-apexcharts'

axios.defaults.baseURL = 'http://localhost:8000/api'
const app = createApp(App)
app.use(router)
app.use(createPinia())
app.use(VueApexCharts)
app.mount('#app')
