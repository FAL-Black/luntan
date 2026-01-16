import { createApp } from 'vue'
import './style.css' // 如果没有 style.css 可以忽略，或者创建它
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
