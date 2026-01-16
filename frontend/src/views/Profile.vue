<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api, { uploadFile, updateAvatar, updateProfile, getMyPosts, deletePost } from '../api';

const user = ref(null);
const myPosts = ref([]);
const activeTab = ref('posts');
const router = useRouter();
const fileInput = ref(null);

const editForm = ref({
    bio: '',
    gender: '',
    location: '',
    website: ''
});

const fetchUserData = async () => {
  try {
    const res = await api.get('/users/me');
    user.value = res.data;
    // Initialize edit form
    editForm.value = {
        bio: user.value.bio || '',
        gender: user.value.gender || '',
        location: user.value.location || '',
        website: user.value.website || ''
    };
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
    await updateAvatar(avatarUrl);
    await fetchUserData();
  } catch (error) {
    alert('头像上传失败');
  }
};

const handleSaveProfile = async () => {
    try {
        await updateProfile(editForm.value);
        alert('资料保存成功');
        await fetchUserData();
        activeTab.value = 'posts';
    } catch (error) {
        alert('保存失败');
    }
};

const handleDeletePost = async (postId) => {
  if (!confirm('确定要删除这条动态吗？')) return;
  try {
    await deletePost(postId);
    myPosts.value = myPosts.value.filter(p => p.id !== postId);
  } catch (error) {
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
        <p class="email">{{ user?.email }}</p>
        <p class="bio">{{ user?.bio || '这个人很懒，什么都没写' }}</p>
        
        <div class="stats-row">
            <span><strong>{{ user?.followers_count || 0 }}</strong> 粉丝</span>
            <span><strong>{{ user?.following_count || 0 }}</strong> 关注</span>
        </div>
        
        <div class="tags">
            <span class="tag" v-if="user?.is_superuser">管理员</span>
            <span class="tag">普通用户</span>
        </div>
      </div>
    </div>

    <div class="actions">
        <button @click="logout" class="btn danger">退出登录</button>
    </div>

    <div class="profile-tabs">
        <button :class="{ active: activeTab === 'posts' }" @click="activeTab = 'posts'">我的动态</button>
        <button :class="{ active: activeTab === 'edit' }" @click="activeTab = 'edit'">编辑资料</button>
    </div>

    <div class="tab-content">
        <div v-if="activeTab === 'posts'" class="my-content">
            <div v-if="myPosts.length === 0" class="empty">暂无动态</div>
            <div v-else class="post-list">
                <div v-for="post in myPosts" :key="post.id" class="post-item">
                    <div class="post-main">
                        <h4>{{ post.title }}</h4>
                        <p>{{ post.content.substring(0, 50) }}...</p>
                        <span class="date">{{ new Date(post.created_at).toLocaleString() }}</span>
                        <div class="post-stats-mini">
                            👀 {{ post.views }} 👍 {{ post.likes_count }}
                        </div>
                    </div>
                    <div class="post-actions">
                        <router-link :to="'/post/' + post.id" class="btn-sm">查看</router-link>
                        <button @click="handleDeletePost(post.id)" class="btn-sm danger">删除</button>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="activeTab === 'edit'" class="edit-section">
            <form @submit.prevent="handleSaveProfile" class="edit-form">
                <div class="form-group">
                    <label>个人简介</label>
                    <textarea v-model="editForm.bio" rows="3" placeholder="介绍一下你自己..."></textarea>
                </div>
                <div class="form-group">
                    <label>性别</label>
                    <select v-model="editForm.gender">
                        <option value="">保密</option>
                        <option value="male">男</option>
                        <option value="female">女</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>所在地</label>
                    <input v-model="editForm.location" type="text" placeholder="城市" />
                </div>
                <div class="form-group">
                    <label>个人网站</label>
                    <input v-model="editForm.website" type="url" placeholder="https://" />
                </div>
                <button type="submit" class="btn primary full-width">保存修改</button>
            </form>
        </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  text-align: center;
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
.avatar-wrapper:hover .avatar-overlay { opacity: 1; }

.info h2 { margin: 0.5rem 0; }
.email { color: #666; margin: 0 0 0.5rem; }
.bio { color: #333; font-style: italic; margin-bottom: 1rem; max-width: 400px; }
.stats-row { display: flex; gap: 1.5rem; margin-bottom: 1rem; color: #555; }
.tags { display: flex; gap: 0.5rem; justify-content: center; }
.tag { background: #f0f2f5; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; color: #666; }

.actions { display: flex; justify-content: center; gap: 1rem; margin-bottom: 2rem; }
.btn { padding: 0.6rem 1.5rem; border: none; border-radius: 20px; cursor: pointer; font-weight: bold; }
.btn.danger { background: #fee; color: #e74c3c; }
.btn.primary { background: #42b983; color: white; }

/* Tabs */
.profile-tabs {
    display: flex;
    border-bottom: 1px solid #eee;
    margin-bottom: 1.5rem;
}
.profile-tabs button {
    flex: 1;
    background: none;
    border: none;
    padding: 1rem;
    cursor: pointer;
    font-size: 1rem;
    color: #666;
    border-bottom: 2px solid transparent;
}
.profile-tabs button.active {
    color: #42b983;
    border-bottom-color: #42b983;
    font-weight: bold;
}

/* Post List */
.post-list { display: flex; flex-direction: column; gap: 1rem; }
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
.date { font-size: 0.8rem; color: #999; margin-right: 1rem; }
.post-stats-mini { font-size: 0.8rem; color: #999; display: inline-block; }
.post-actions { display: flex; gap: 0.5rem; }
.btn-sm { padding: 0.4rem 0.8rem; border: none; border-radius: 4px; cursor: pointer; font-size: 0.8rem; text-decoration: none; color: #333; background: #eee; }
.btn-sm.danger { background: #ffebeb; color: #e74c3c; }

/* Edit Form */
.edit-section { max-width: 500px; margin: 0 auto; }
.form-group { margin-bottom: 1rem; text-align: left; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
.form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 8px;
}
.full-width { width: 100%; }

.empty { color: #999; text-align: center; padding: 2rem; }

@media (max-width: 480px) {
  .profile-container { padding: 1.5rem; margin: 1rem; }
  .post-item { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .post-actions { width: 100%; display: flex; justify-content: flex-end; }
}
</style>
