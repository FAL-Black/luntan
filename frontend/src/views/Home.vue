<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const user = ref(null);
const router = useRouter();

const fetchUserInfo = async () => {
  try {
    const res = await api.get('/users/me');
    user.value = res.data;
  } catch (error) {
    // 获取失败可能是 token 过期或未登录，不用弹窗，静默失败即可
    // 拦截器会自动处理 401 跳转
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  user.value = null;
  router.push('/login');
};

onMounted(() => {
  if (localStorage.getItem('token')) {
    fetchUserInfo();
  }
});
</script>

<template>
  <div class="home-container">
    <h1>欢迎来到技术论坛</h1>
    
    <div v-if="user" class="user-info">
      <p>你好，<strong>{{ user.username }}</strong>！</p>
      <p>你的邮箱: {{ user.email }}</p>
      <button @click="logout" class="logout-btn">退出登录</button>
    </div>
    
    <div v-else class="guest-info">
      <p>请先登录以查看更多内容。</p>
      <div class="actions">
        <router-link to="/login" class="btn">登录</router-link>
        <router-link to="/register" class="btn secondary">注册</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 2rem auto;
  text-align: center;
}
.user-info {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-top: 2rem;
}
.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}
.guest-info {
  margin-top: 2rem;
}
.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}
.btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #42b983;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
.btn.secondary {
  background-color: #6c757d;
}
</style>
