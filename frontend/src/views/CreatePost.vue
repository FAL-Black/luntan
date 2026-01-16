<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createPost } from '../api';

const title = ref('');
const content = ref('');
const errorMsg = ref('');
const router = useRouter();

const handleCreatePost = async () => {
  if (!title.value || !content.value) {
    errorMsg.value = '标题和内容不能为空';
    return;
  }
  
  try {
    await createPost({
      title: title.value,
      content: content.value
    });
    router.push('/');
  } catch (error) {
    console.error(error);
    errorMsg.value = '发布失败，请重试';
  }
};
</script>

<template>
  <div class="create-post-container">
    <h2>发布新帖子</h2>
    <form @submit.prevent="handleCreatePost">
      <div class="form-group">
        <label>标题</label>
        <input v-model="title" type="text" placeholder="请输入标题" required />
      </div>
      <div class="form-group">
        <label>内容</label>
        <textarea v-model="content" placeholder="请输入内容" rows="6" required></textarea>
      </div>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <div class="actions">
        <button type="submit" class="btn primary">发布</button>
        <router-link to="/" class="btn secondary">取消</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-post-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1.5rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: inherit;
}
.actions {
  display: flex;
  gap: 1rem;
}
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  font-size: 1rem;
}
.btn.primary {
  background-color: #42b983;
  color: white;
}
.btn.secondary {
  background-color: #6c757d;
  color: white;
}
.error {
  color: red;
  margin-bottom: 1rem;
}
</style>
