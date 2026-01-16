<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createPost, uploadFile } from '../api';

const title = ref('');
const content = ref('');
const category = ref('');
const tags = ref('');
const isOriginal = ref(true);
const selectedFile = ref(null);
const previewUrl = ref(null);
const isUploading = ref(false);
const errorMsg = ref('');
const router = useRouter();

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    // 创建本地预览 URL
    previewUrl.value = URL.createObjectURL(file);
  }
};

const handleCreatePost = async () => {
  if (!title.value || !content.value) {
    errorMsg.value = '标题和内容不能为空';
    return;
  }
  
  isUploading.value = true;
  let imageUrl = null;

  try {
    // 1. 如果有文件，先上传
    if (selectedFile.value) {
      const uploadRes = await uploadFile(selectedFile.value);
      imageUrl = uploadRes.data.url;
    }

    // 2. 创建帖子
    await createPost({
      title: title.value,
      content: content.value,
      image_url: imageUrl,
      category: category.value || '未分类',
      tags: tags.value,
      is_original: isOriginal.value
    });
    
    router.push('/');
  } catch (error) {
    console.error(error);
    errorMsg.value = '发布失败，请重试';
  } finally {
    isUploading.value = false;
  }
};
</script>

<template>
  <div class="create-post-container">
    <div class="header">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      <h2>发布新动态</h2>
    </div>
    
    <form @submit.prevent="handleCreatePost" class="post-form">
      <div class="form-group">
        <input v-model="title" type="text" placeholder="起个标题..." required class="title-input" />
      </div>
      
      <div class="form-group">
        <textarea v-model="content" placeholder="分享你的新鲜事..." rows="6" required class="content-input"></textarea>
      </div>

      <div class="meta-row">
        <div class="form-group half">
            <select v-model="category" class="select-input">
                <option value="">选择分类</option>
                <option value="技术">技术</option>
                <option value="生活">生活</option>
                <option value="闲聊">闲聊</option>
                <option value="分享">分享</option>
            </select>
        </div>
        <div class="form-group half">
            <input v-model="tags" type="text" placeholder="标签 (用逗号分隔)" class="tags-input" />
        </div>
      </div>

      <div class="options-row">
        <label class="checkbox-label">
            <input type="checkbox" v-model="isOriginal"> 声明原创
        </label>
      </div>

      <div class="image-upload-section">
        <label for="file-upload" class="upload-btn">
          📷 添加图片
        </label>
        <input id="file-upload" type="file" @change="handleFileChange" accept="image/*" style="display: none;" />
        
        <div v-if="previewUrl" class="image-preview">
          <img :src="previewUrl" alt="Preview" />
          <button @click.prevent="selectedFile = null; previewUrl = null" class="remove-btn">×</button>
        </div>
      </div>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      
      <div class="actions">
        <button type="submit" class="submit-btn" :disabled="isUploading">
          {{ isUploading ? '发布中...' : '发布' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-post-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}
.back-link {
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}
.header h2 {
  margin: 0;
  font-size: 1.5rem;
}
.post-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.title-input {
  width: 100%;
  font-size: 1.5rem;
  font-weight: bold;
  border: none;
  border-bottom: 1px solid #eee;
  padding: 0.5rem 0;
  outline: none;
}
.content-input {
  width: 100%;
  font-size: 1.1rem;
  border: none;
  resize: none;
  outline: none;
  font-family: inherit;
  line-height: 1.6;
}

.meta-row {
    display: flex;
    gap: 1rem;
}
.half { flex: 1; }
.select-input, .tags-input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #eee;
    border-radius: 8px;
    background: #f9f9f9;
}

.options-row {
    margin-bottom: 0.5rem;
}
.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: 0.9rem;
    color: #666;
}

.upload-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #f0f2f5;
  color: #666;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}
.upload-btn:hover {
  background: #e4e6eb;
}
.image-preview {
  position: relative;
  margin-top: 1rem;
  display: inline-block;
}
.image-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}
.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: rgba(0,0,0,0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.submit-btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.8rem 3rem;
  border-radius: 24px;
  font-weight: bold;
  cursor: pointer;
  float: right;
  transition: background 0.2s;
  font-size: 1.1rem;
}
.submit-btn:hover:not(:disabled) {
  background: #3aa876;
}
.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.error {
  color: #e74c3c;
  font-size: 0.9rem;
}
</style>
