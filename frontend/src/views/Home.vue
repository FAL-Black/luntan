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
      <div class="logo">
        <span class="logo-icon">✒️</span> 某某博客
      </div>
      <div v-if="user" class="user-actions">
        <router-link to="/create-post" class="btn primary round">＋ 发布文章</router-link>
        <div class="user-menu">
            <span class="username">{{ user.username }}</span>
            <router-link to="/profile" class="btn text">个人中心</router-link>
            <button @click="logout" class="btn text danger">退出</button>
        </div>
      </div>
      <div v-else class="guest-actions">
        <router-link to="/login" class="btn text">登录</router-link>
        <router-link to="/register" class="btn primary round">注册</router-link>
      </div>
    </header>

    <div class="main-layout">
        <main class="feed">
            <!-- 轮播 Banner (Mock) -->
            <div class="banner-carousel">
                <div class="banner-item active">
                    <div class="banner-content">
                        <h2>分享技术，记录生活</h2>
                        <p>加入我们要的技术社区，开启创作之旅</p>
                    </div>
                </div>
            </div>

            <div v-if="posts.length === 0" class="empty-state">
                还没有动态，去发布第一条吧！
            </div>
            
            <div v-for="post in posts" :key="post.id" class="post-card" :class="{ pinned: post.is_pinned }">
                <div class="post-header">
                    <div class="avatar-placeholder">{{ (post.owner_username || 'U')[0].toUpperCase() }}</div>
                    <div class="post-info">
                        <span class="author-name">{{ post.owner_username || 'Unknown' }}</span>
                        <div class="meta-row">
                            <span class="post-time">{{ formatDate(post.created_at) }}</span>
                            <span v-if="post.is_pinned" class="tag pinned">置顶</span>
                            <span v-if="post.is_original" class="tag original">原创</span>
                        </div>
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
                    <div class="stats">
                        <span class="stat-item">👀 {{ post.views || 0 }}</span>
                        <span class="stat-item">👍 {{ post.likes_count || 0 }}</span>
                        <span class="stat-item">💬 {{ post.comments_count || 0 }}</span>
                    </div>
                    <router-link :to="'/post/' + post.id" class="action-btn">
                        查看详情 →
                    </router-link>
                </div>
            </div>
        </main>

        <aside class="sidebar">
            <div class="widget">
                <h3>热门标签</h3>
                <div class="tags-cloud">
                    <span class="tag-pill">Python</span>
                    <span class="tag-pill">Vue3</span>
                    <span class="tag-pill">FastAPI</span>
                    <span class="tag-pill">生活</span>
                    <span class="tag-pill">随笔</span>
                </div>
            </div>
            
            <div class="widget">
                <h3>推荐作者</h3>
                <ul class="user-list">
                    <li>
                        <div class="mini-avatar">A</div>
                        <span>Admin</span>
                    </li>
                    <!-- Mock Data -->
                </ul>
            </div>

            <div class="widget copyright">
                <p>© 2026 某某博客</p>
                <p>ICP备88888888号</p>
            </div>
        </aside>
    </div>
    
    <!-- 回到顶部按钮 (CSS 实现) -->
    <a href="#" class="back-to-top">↑</a>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px; /* 1200px PC 适配 */
  margin: 0 auto;
  min-height: 100vh;
  background: #f8fafc;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}
.logo {
  font-size: 1.5rem;
  font-weight: 900;
  color: #2563eb; /* Brand Blue */
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.main-layout {
    display: flex;
    gap: 2rem;
    padding: 2rem;
    align-items: flex-start;
}

.feed {
    flex: 1;
    min-width: 0;
}

.sidebar {
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

/* Banner */
.banner-carousel {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    border-radius: 12px;
    padding: 3rem;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.banner-content h2 { margin: 0 0 1rem; font-size: 2rem; }
.banner-content p { margin: 0; opacity: 0.9; }

/* Post Card */
.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e2e8f0;
}
.post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.post-card.pinned {
    border-left: 4px solid #ef4444;
}

.post-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}
.avatar-placeholder {
    width: 40px;
    height: 40px;
    background: #2563eb;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 12px;
}
.author-name {
    font-weight: bold;
    color: #1e293b;
    display: block;
}
.meta-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #64748b;
}
.tag {
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.7rem;
}
.tag.pinned { background: #fee2e2; color: #ef4444; }
.tag.original { background: #dbeafe; color: #2563eb; }

.post-title {
    font-size: 1.25rem;
    margin: 0 0 0.5rem;
    color: #1e293b;
}
.post-text {
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.post-content-link {
    text-decoration: none;
    display: block;
}
.post-image img {
    max-width: 100%;
    border-radius: 8px;
    max-height: 300px;
    object-fit: cover;
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
}
.stats {
    display: flex;
    gap: 1.5rem;
    color: #94a3b8;
    font-size: 0.9rem;
}
.action-btn {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
}

/* Sidebar Widgets */
.widget {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}
.widget h3 {
    margin: 0 0 1rem;
    font-size: 1rem;
    color: #1e293b;
    border-left: 4px solid #2563eb;
    padding-left: 0.8rem;
}
.tags-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.tag-pill {
    background: #f1f5f9;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    color: #475569;
    cursor: pointer;
    transition: background 0.2s;
}
.tag-pill:hover { background: #e2e8f0; }

.user-list li {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f1f5f9;
}
.mini-avatar {
    width: 30px;
    height: 30px;
    background: #cbd5e1;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
}
.copyright {
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 0.85rem;
    padding: 0;
}

/* Back to top */
.back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 40px;
    height: 40px;
    background: #2563eb;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
    opacity: 0.8;
    transition: opacity 0.2s;
}
.back-to-top:hover { opacity: 1; }

/* Responsive */
@media (max-width: 900px) {
    .main-layout {
        flex-direction: column;
    }
    .sidebar {
        width: 100%;
        order: -1; /* Sidebar on top on mobile or bottom? Design doc says bottom usually or hidden in menu. But let's keep it simple. */
        display: none; /* Hide sidebar on mobile for simplicity */
    }
    .home-container { padding: 0; }
    .main-layout { padding: 1rem; }
}
</style>
