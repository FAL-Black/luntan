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
      <div class="logo">Luntan</div>
      <div v-if="user" class="user-actions">
        <router-link to="/create-post" class="btn primary round">＋ 发动态</router-link>
        <div class="user-menu">
            <span class="username">{{ user.username }}</span>
            <router-link to="/profile" class="btn text">主页</router-link>
            <button @click="logout" class="btn text danger">退出</button>
        </div>
      </div>
      <div v-else class="guest-actions">
        <router-link to="/login" class="btn text">登录</router-link>
        <router-link to="/register" class="btn primary round">注册</router-link>
      </div>
    </header>

    <main class="feed">
      <div v-if="posts.length === 0" class="empty-state">
        还没有动态，去发布第一条吧！
      </div>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <div class="post-header">
            <div class="avatar-placeholder">{{ (post.owner_username || 'U')[0].toUpperCase() }}</div>
            <div class="post-info">
                <span class="author-name">{{ post.owner_username || 'Unknown' }}</span>
                <span class="post-time">{{ formatDate(post.created_at) }}</span>
            </div>
        </div>
        
        <router-link :to="'/post/' + post.id" class="post-content-link">
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-text">{{ post.content.substring(0, 150) }}{{ post.content.length > 150 ? '...' : '' }}</p>
            <div v-if="post.image_url" class="post-image">
                <img :src="post.image_url" alt="Post image" loading="lazy" />
            </div>
        </router-link>

        <div class="post-footer">
            <router-link :to="'/post/' + post.id" class="action-btn">
                💬 评论
            </router-link>
            <button class="action-btn">👍 点赞</button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 700px;
  margin: 0 auto;
  padding-bottom: 2rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid #eee;
}
.logo {
  font-size: 1.5rem;
  font-weight: 900;
  color: #42b983;
}
.user-actions, .guest-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.user-menu {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.username {
    font-weight: bold;
    margin-right: 0.5rem;
}

.btn {
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.95rem;
  transition: all 0.2s;
}
.btn.round { border-radius: 20px; }
.btn.primary { background-color: #42b983; color: white; }
.btn.primary:hover { background-color: #3aa876; }
.btn.text { background: none; color: #666; padding: 0.5rem; }
.btn.text:hover { color: #333; background: #f5f5f5; border-radius: 4px;}
.btn.danger:hover { color: #e74c3c; }

.feed {
  padding: 1rem;
}
.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}
.post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.post-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}
.avatar-placeholder {
    width: 40px;
    height: 40px;
    background: #42b983;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 10px;
}
.post-info {
    display: flex;
    flex-direction: column;
}
.author-name {
    font-weight: bold;
    font-size: 1rem;
    color: #333;
}
.post-time {
    font-size: 0.8rem;
    color: #999;
}
.post-content-link {
    text-decoration: none;
    color: inherit;
    display: block;
}
.post-title {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
}
.post-text {
    font-size: 1rem;
    line-height: 1.6;
    color: #444;
    margin-bottom: 1rem;
}
.post-image img {
    max-width: 100%;
    border-radius: 8px;
    max-height: 400px;
    object-fit: cover;
}
.post-footer {
    border-top: 1px solid #f0f0f0;
    margin-top: 1rem;
    padding-top: 0.8rem;
    display: flex;
    justify-content: space-around;
}
.action-btn {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 5px;
    text-decoration: none;
}
.action-btn:hover {
    color: #42b983;
}
</style>
