<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api, { uploadFile, updateAvatar, getMyPosts, deletePost } from '../api';

const user = ref(null);
const myPosts = ref([]);
const router = useRouter();
const fileInput = ref(null);

const fetchUserData = async () => {
  try {
    const res = await api.get('/users/me');
    user.value = res.data;
  } catch (error) {
    router.push('/login');
  }
};

const fetchUserPosts = async () => {
  try {
    const res = await getMyPosts();
    myPosts.value = res.data;
  } catch (error) {
    console.error('Failed to fetch my posts', error);
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  router.push('/login');
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const uploadRes = await uploadFile(file);
    const avatarUrl = uploadRes.data.url;
    
    // 更新用户头像
    await updateAvatar(avatarUrl);
    
    // 刷新用户信息
    await fetchUserData();
  } catch (error) {
    console.error('Avatar upload failed', error);
    alert('头像上传失败');
  }
};

const handleDeletePost = async (postId) => {
  if (!confirm('确定要删除这条动态吗？')) return;
  
  try {
    await deletePost(postId);
    // 从列表中移除
    myPosts.value = myPosts.value.filter(p => p.id !== postId);
  } catch (error) {
    console.error('Delete failed', error);
    alert('删除失败');
  }
};

onMounted(() => {
  fetchUserData();
  fetchUserPosts();
});
</script>

<template>
  <div class="profile-container">
    <div class="profile-header">
      <div class="avatar-wrapper" @click="triggerFileInput">
        <img v-if="user?.avatar_url" :src="user.avatar_url" class="avatar-img" />
        <div v-else class="avatar-large">{{ user?.username?.[0].toUpperCase() }}</div>
        <div class="avatar-overlay">更换头像</div>
      </div>
      <input 
        ref="fileInput" 
        type="file" 
        accept="image/*" 
        style="display: none" 
        @change="handleAvatarChange" 
      />
      
      <div class="info">
        <h2>{{ user?.username }}</h2>
        <p>{{ user?.email }}</p>
        <div class="tags">
            <span class="tag" v-if="user?.is_superuser">管理员</span>
            <span class="tag">普通用户</span>
        </div>
      </div>
    </div>

    <div class="actions">
        <button @click="logout" class="btn danger">退出登录</button>
    </div>

    <div class="my-content">
        <h3>我的动态 ({{ myPosts.length }})</h3>
        <div v-if="myPosts.length === 0" class="empty">暂无动态</div>
        <div v-else class="post-list">
            <div v-for="post in myPosts" :key="post.id" class="post-item">
                <div class="post-main">
                    <h4>{{ post.title }}</h4>
                    <p>{{ post.content.substring(0, 50) }}...</p>
                    <span class="date">{{ new Date(post.created_at).toLocaleString() }}</span>
                </div>
                <button @click="handleDeletePost(post.id)" class="btn-sm danger">删除</button>
            </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  text-align: center;
}
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}
.avatar-wrapper {
  position: relative;
  cursor: pointer;
  width: 100px;
  height: 100px;
  margin-bottom: 1rem;
}
.avatar-large, .avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
.avatar-large {
  background: #42b983;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
}
.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  font-size: 0.8rem;
}
.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.info h2 { margin: 0.5rem 0; }
.info p { color: #666; margin: 0; }
.tags { margin-top: 0.5rem; display: flex; gap: 0.5rem; justify-content: center; }
.tag {
    background: #f0f2f5;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    color: #666;
}
.actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.btn {
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
}
.btn.danger { background: #fee; color: #e74c3c; }

.my-content {
    text-align: left;
    border-top: 1px solid #eee;
    padding-top: 1rem;
}
.post-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.post-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: #f9f9f9;
    border-radius: 8px;
}
.post-main h4 { margin: 0 0 0.5rem; }
.post-main p { margin: 0; color: #666; font-size: 0.9rem; }
.date { font-size: 0.8rem; color: #999; }
.btn-sm {
    padding: 0.4rem 0.8rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
}
.btn-sm.danger { background: #ffebeb; color: #e74c3c; }
.btn-sm.danger:hover { background: #ffdada; }
.empty { color: #999; text-align: center; padding: 2rem; }

@media (max-width: 480px) {
  .profile-container {
    padding: 1.5rem;
    margin: 1rem;
  }
}
</style>
