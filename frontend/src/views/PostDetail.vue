<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getPost, getComments, createComment, likePost, collectPost, followUser } from '../api';

const route = useRoute();
const router = useRouter();
const postId = route.params.id;

const post = ref(null);
const comments = ref([]);
const newCommentContent = ref('');
const user = ref(localStorage.getItem('username'));
const isFollowing = ref(false);

const fetchPostData = async () => {
  try {
    const postRes = await getPost(postId);
    post.value = postRes.data;
    
    // Check if following author (Mock check, ideally should be from API)
    // Actually we need to fetch author profile to check following status or returned in post
    // For now, let's assume post.owner has following status if we updated backend correctly?
    // Backend Post schema doesn't have owner.is_following. 
    // We'll leave follow status check for now or fetch author profile.
    
    const commentsRes = await getComments(postId);
    comments.value = commentsRes.data;
  } catch (error) {
    console.error('获取帖子详情失败', error);
  }
};

const handleCommentSubmit = async () => {
  if (!newCommentContent.value.trim()) return;
  
  try {
    await createComment(postId, newCommentContent.value);
    newCommentContent.value = '';
    // 重新获取评论列表
    const commentsRes = await getComments(postId);
    comments.value = commentsRes.data;
    // Update comment count locally
    if (post.value) post.value.comments_count++;
  } catch (error) {
    alert('评论失败，请先登录');
    router.push('/login');
  }
};

const handleLike = async () => {
    try {
        const res = await likePost(postId);
        post.value.is_liked = res.data.is_liked;
        post.value.likes_count += res.data.is_liked ? 1 : -1;
    } catch (error) {
        if (error.response && error.response.status === 401) router.push('/login');
    }
};

const handleCollect = async () => {
    try {
        const res = await collectPost(postId);
        post.value.is_collected = res.data.is_collected;
    } catch (error) {
        if (error.response && error.response.status === 401) router.push('/login');
    }
};

const handleFollow = async () => {
    if (!post.value) return;
    try {
        const res = await followUser(post.value.owner_id);
        isFollowing.value = res.data.is_following; // This needs to be managed better
        alert(res.data.is_following ? '关注成功' : '已取消关注');
    } catch (error) {
         if (error.response && error.response.status === 401) router.push('/login');
         else alert('操作失败');
    }
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString();
};

onMounted(() => {
  fetchPostData();
});
</script>

<template>
  <div class="post-detail-container">
    <div class="actions">
        <router-link to="/" class="btn secondary small">← 返回首页</router-link>
    </div>

    <div v-if="post" class="main-content">
        <!-- 左侧文章区 -->
        <article class="post-card">
            <h1 class="post-title">{{ post.title }}</h1>
            
            <div class="post-meta-top">
                <span class="tag original" v-if="post.is_original">原创</span>
                <span class="meta-item">{{ formatDate(post.created_at) }}</span>
                <span class="meta-item">阅读 {{ post.views }}</span>
            </div>

            <div class="post-body">
                <div v-if="post.image_url" class="post-banner">
                    <img :src="post.image_url" alt="Cover" />
                </div>
                <div class="text-content">{{ post.content }}</div>
            </div>

            <div class="post-footer-actions">
                <button class="action-btn" :class="{ active: post.is_liked }" @click="handleLike">
                    <span class="icon">👍</span> {{ post.likes_count || '点赞' }}
                </button>
                <button class="action-btn" :class="{ active: post.is_collected }" @click="handleCollect">
                    <span class="icon">⭐</span> {{ post.is_collected ? '已收藏' : '收藏' }}
                </button>
            </div>
        </article>

        <!-- 评论区 -->
        <div class="comments-section">
            <h3>评论 ({{ comments.length }})</h3>
            
            <div v-if="user" class="comment-form">
                <textarea 
                    v-model="newCommentContent" 
                    placeholder="友善评论是交流的起点..." 
                    rows="3"
                ></textarea>
                <button @click="handleCommentSubmit" class="btn primary small">发表评论</button>
            </div>
            <div v-else class="login-tip">
                <router-link to="/login">登录</router-link> 后参与评论
            </div>

            <div class="comment-list">
                <div v-for="comment in comments" :key="comment.id" class="comment-item">
                    <div class="comment-avatar">
                        {{ (comment.owner_username || 'U')[0].toUpperCase() }}
                    </div>
                    <div class="comment-content">
                        <div class="comment-header">
                            <strong>{{ comment.owner_username || '用户' + comment.owner_id }}</strong>
                            <span class="date">{{ formatDate(comment.created_at) }}</span>
                        </div>
                        <div class="comment-text">
                            {{ comment.content }}
                        </div>
                    </div>
                </div>
                <div v-if="comments.length === 0" class="no-comments">
                    暂无评论，抢沙发！
                </div>
            </div>
        </div>
    </div>

    <!-- 右侧侧边栏 -->
    <aside v-if="post" class="sidebar">
        <div class="author-card">
            <div class="author-header">
                <div class="avatar-large">{{ (post.owner_username || 'U')[0].toUpperCase() }}</div>
                <div class="author-info">
                    <h3>{{ post.owner_username }}</h3>
                    <p>暂无简介</p>
                </div>
            </div>
            <div class="author-stats">
                <div class="stat">
                    <strong>{{ post.posts_count || 0 }}</strong>
                    <span>文章</span>
                </div>
                <div class="stat">
                    <strong>0</strong>
                    <span>粉丝</span>
                </div>
            </div>
            <button class="btn primary full-width" @click="handleFollow">
                {{ isFollowing ? '已关注' : '+ 关注' }}
            </button>
        </div>
    </aside>
  </div>
</template>

<style scoped>
.post-detail-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem;
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}
.main-content {
    flex: 1;
    min-width: 0; /* 防止 flex item 溢出 */
}
.sidebar {
    width: 300px;
    position: sticky;
    top: 2rem;
}

/* Post Card */
.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.post-title {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    color: #333;
}
.post-meta-top {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: #999;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}
.tag.original {
    background: #e3f2fd;
    color: #2196f3;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8rem;
}
.post-banner img {
    max-width: 100%;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}
.text-content {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #333;
    white-space: pre-wrap;
}

.post-footer-actions {
    margin-top: 3rem;
    display: flex;
    justify-content: center;
    gap: 2rem;
}
.action-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 2rem;
    border-radius: 30px;
    border: 1px solid #ddd;
    background: #fff;
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.2s;
}
.action-btn:hover { background: #f5f5f5; }
.action-btn.active {
    color: #f97316;
    border-color: #f97316;
    background: #fff7ed;
}

/* Author Card */
.author-card {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.author-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
.avatar-large {
    width: 60px;
    height: 60px;
    background: #42b983;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
}
.author-info h3 { margin: 0 0 0.2rem; font-size: 1.1rem; }
.author-info p { margin: 0; color: #999; font-size: 0.8rem; }
.author-stats {
    display: flex;
    justify-content: space-around;
    margin-bottom: 1.5rem;
    text-align: center;
}
.stat strong { display: block; font-size: 1.2rem; color: #333; }
.stat span { color: #999; font-size: 0.8rem; }
.full-width { width: 100%; }

/* Comments */
.comments-section {
    background: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.comment-form textarea {
    width: 100%;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 1rem;
    resize: vertical;
}
.comment-item {
    display: flex;
    gap: 1rem;
    padding: 1.5rem 0;
    border-bottom: 1px solid #eee;
}
.comment-avatar {
    width: 40px;
    height: 40px;
    background: #eee;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.comment-content { flex: 1; }
.comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.comment-text { color: #555; line-height: 1.5; }

@media (max-width: 768px) {
    .post-detail-container {
        flex-direction: column;
    }
    .sidebar {
        width: 100%;
        position: static;
        order: -1; /* Put author info on top for mobile */
    }
}
</style>
