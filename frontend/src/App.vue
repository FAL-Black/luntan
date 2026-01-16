<script setup>
import { ref, onMounted } from 'vue'

const message = ref('正在连接后端...')
const serverInfo = ref(null)

const fetchData = async () => {
  try {
    // 使用相对路径，通过 Nginx 代理访问
    // 对应后端 /api/ 路由
    const res = await fetch('/api/')
    if (!res.ok) throw new Error(res.statusText)
    const data = await res.json()
    message.value = data.message
  } catch (error) {
    message.value = '连接后端失败: ' + error.message
    console.error('API Error:', error)
  }

  try {
    const res = await fetch('/api/info')
    if (res.ok) {
        serverInfo.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="app-container">
    <h1>论坛开发环境</h1>
    
    <div class="status-card">
      <h2>系统状态</h2>
      <div class="status-item">
        <strong>后端连接:</strong>
        <span :class="{ 'success': !message.includes('失败'), 'error': message.includes('失败') }">
          {{ message }}
        </span>
      </div>
      
      <div v-if="serverInfo" class="server-info">
        <p>论坛名称: {{ serverInfo.forum_name }}</p>
        <p>版本: {{ serverInfo.version }}</p>
        <p>状态: {{ serverInfo.status }}</p>
      </div>
    </div>

    <p class="guide">
      请确保后端服务已启动: <br>
      <code>cd backend && uvicorn main:app --reload</code>
    </p>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  text-align: center;
}

.status-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.status-item {
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.success {
  color: #28a745;
  font-weight: bold;
}

.error {
  color: #dc3545;
  font-weight: bold;
}

.guide {
  color: #6c757d;
  background: #f1f3f5;
  padding: 1rem;
  border-radius: 4px;
  display: inline-block;
}

code {
  background: #343a40;
  color: #fff;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
</style>
