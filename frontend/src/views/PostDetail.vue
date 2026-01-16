<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getPost, getComments, createComment } from '../api';

const route = useRoute();
const router = useRouter();
const postId = route.params.id;

const post = ref(null);
const comments = ref([]);
const newCommentContent = ref('');
const user = ref(localStorage.getItem('username'));

const fetchPostData = async () => {
  try {
    const postRes = await getPost(postId);
    post.value = postRes.data;
    
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
  } catch (error) {
    alert('评论失败，请先登录');
    router.push('/login');
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

    <div v-if="post" class="post-content-card">
      <h1>{{ post.title }}</h1>
      <div class="meta">
        <span>作者ID: {{ post.owner_id }}</span>
        <span>发布于: {{ formatDate(post.created_at) }}</span>
      </div>
      <div class="content-body">
        {{ post.content }}
      </div>
    </div>

    <div class="comments-section">
      <h3>评论 ({{ comments.length }})</h3>
      
      <div v-if="user" class="comment-form">
        <textarea 
            v-model="newCommentContent" 
            placeholder="写下你的评论..." 
            rows="3"
        ></textarea>
        <button @click="handleCommentSubmit" class="btn primary small">发表评论</button>
      </div>
      <div v-else class="login-tip">
        <router-link to="/login">登录</router-link> 后参与评论
      </div>

      <div class="comment-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <strong>{{ comment.owner_username || '用户' + comment.owner_id }}</strong>
            <span class="date">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-body">
            {{ comment.content }}
          </div>
        </div>
        <div v-if="comments.length === 0" class="no-comments">
            暂无评论，抢沙发！
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}
.actions {
  margin-bottom: 1rem;
}
.post-content-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.meta {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  display: flex;
  gap: 1rem;
}
.content-body {
  font-size: 1.1rem;
  line-height: 1.6;
  white-space: pre-wrap; /* 保留换行 */
}

.comments-section {
  margin-top: 2rem;
}
.comment-form {
  margin-bottom: 2rem;
}
.comment-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  font-family: inherit;
  resize: vertical;
}
.login-tip {
  background: #f8f9fa;
  padding: 1rem;
  text-align: center;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
.date {
  color: #999;
}
.no-comments {
  text-align: center;
  color: #999;
  padding: 2rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9rem;
  display: inline-block;
}
.btn.primary { background-color: #42b983; color: white; }
.btn.secondary { background-color: #6c757d; color: white; }
</style>
