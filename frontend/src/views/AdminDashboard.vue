<script setup>
import { ref, onMounted } from 'vue';
import { getAllUsers, getPosts, deletePost } from '../api';

const users = ref([]);
const posts = ref([]);
const activeTab = ref('users'); // users | posts

const fetchUsers = async () => {
  try {
    const res = await getAllUsers();
    users.value = res.data;
  } catch (error) {
    console.error(error);
  }
};

const fetchAllPosts = async () => {
  try {
    const res = await getPosts();
    posts.value = res.data;
  } catch (error) {
    console.error(error);
  }
};

const handleDeletePost = async (postId) => {
    if(!confirm('确定要删除此帖子吗？')) return;
    try {
        await deletePost(postId);
        posts.value = posts.value.filter(p => p.id !== postId);
    } catch (error) {
        alert('删除失败');
    }
};

onMounted(() => {
  fetchUsers();
  fetchAllPosts();
});
</script>

<template>
  <div class="admin-container">
    <h1>管理后台</h1>
    
    <div class="tabs">
      <button :class="{ active: activeTab === 'users' }" @click="activeTab = 'users'">用户管理</button>
      <button :class="{ active: activeTab === 'posts' }" @click="activeTab = 'posts'">帖子管理</button>
    </div>

    <div v-if="activeTab === 'users'" class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>状态</th>
            <th>角色</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>
                <div class="user-cell">
                    <img :src="user.avatar_url || 'https://via.placeholder.com/30'" class="avatar-mini" />
                    {{ user.username }}
                </div>
            </td>
            <td>{{ user.email }}</td>
            <td>
                <span :class="['status', user.is_active ? 'active' : 'inactive']">
                    {{ user.is_active ? '正常' : '封禁' }}
                </span>
            </td>
            <td>{{ user.is_superuser ? '管理员' : '用户' }}</td>
            <td>
              <button class="btn-sm danger">封禁</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-else class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>标题</th>
                    <th>作者</th>
                    <th>发布时间</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="post in posts" :key="post.id">
                    <td>{{ post.id }}</td>
                    <td class="title-cell" :title="post.title">{{ post.title }}</td>
                    <td>{{ post.owner_username }}</td>
                    <td>{{ new Date(post.created_at).toLocaleString() }}</td>
                    <td>
                        <button @click="handleDeletePost(post.id)" class="btn-sm danger">删除</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 2rem;
}
.tabs {
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #ddd;
}
.tabs button {
    background: none;
    border: none;
    padding: 1rem 2rem;
    font-size: 1rem;
    cursor: pointer;
    color: #666;
    border-bottom: 2px solid transparent;
}
.tabs button.active {
    color: #42b983;
    border-bottom-color: #42b983;
    font-weight: bold;
}
.table-wrapper {
    overflow-x: auto;
}
table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #eee;
}
th { background: #f8f9fa; font-weight: 600; }
.status.active { color: green; }
.status.inactive { color: red; }
.btn-sm {
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
}
.btn-sm.danger { background: #fee; color: #e74c3c; }
.user-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.avatar-mini {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    object-fit: cover;
}
.title-cell {
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
    margin: 1rem auto;
  }
  .tabs button {
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
