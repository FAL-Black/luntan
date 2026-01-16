<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api, { getPosts } from '../api';

const user = ref(null);
const posts = ref([]);
const router = useRouter();

const fetchUserInfo = async () => {
  try {
    const res = await api.get('/users/me');
    user.value = res.data;
  } catch (error) {
    // 静默失败
  }
};

const fetchPosts = async () => {
  try {
    const res = await getPosts();
    posts.value = res.data;
  } catch (error) {
    console.error('获取帖子列表失败', error);
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  user.value = null;
  router.push('/login');
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString();
};

onMounted(() => {
  if (localStorage.getItem('token')) {
    fetchUserInfo();
  }
  fetchPosts();
});
</script>

<template>
  <div class="home-container">
    <header class="header">
      <h1>技术论坛</h1>
      <div v-if="user" class="user-actions">
        <span>欢迎, {{ user.username }}</span>
        <router-link to="/create-post" class="btn primary small">发布帖子</router-link>
        <button @click="logout" class="btn danger small">退出</button>
      </div>
      <div v-else class="guest-actions">
        <router-link to="/login" class="btn primary small">登录</router-link>
        <router-link to="/register" class="btn secondary small">注册</router-link>
      </div>
    </header>

    <main class="post-list">
      <h2>最新帖子</h2>
      <div v-if="posts.length === 0" class="empty-state">
        暂无帖子，快来发布第一条吧！
      </div>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h3>{{ post.title }}</h3>
        <p class="post-content">{{ post.content }}</p>
        <div class="post-meta">
          <span>作者ID: {{ post.owner_id }}</span>
          <span>发布时间: {{ formatDate(post.created_at) }}</span>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  margin-left: 0.5rem;
  font-size: 0.9rem;
}
.btn.primary { background-color: #42b983; color: white; }
.btn.secondary { background-color: #6c757d; color: white; }
.btn.danger { background-color: #dc3545; color: white; }

.post-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.post-card h3 { margin-top: 0; }
.post-meta {
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #6c757d;
  display: flex;
  gap: 1rem;
  align-items: center;
}
.post-title-link {
  color: #2c3e50;
  text-decoration: none;
}
.post-title-link:hover {
  color: #42b983;
}
.read-more {
  margin-left: auto;
  color: #42b983;
  text-decoration: none;
}
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 8px;
}
</style>
