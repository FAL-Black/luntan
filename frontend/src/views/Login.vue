<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api';

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const successMsg = ref('');
const isLoading = ref(false);
const router = useRouter();
const route = useRoute();

onMounted(() => {
    if (route.query.registered === 'true') {
        successMsg.value = '注册成功！请登录';
    }
});

const handleLogin = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  isLoading.value = true;
  try {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);

    const res = await api.post('/token', formData);
    
    localStorage.setItem('token', res.data.access_token);
    localStorage.setItem('username', username.value);
    
    // 获取用户信息以判断是否为管理员
    const userRes = await api.get('/users/me');
    if (userRes.data.is_superuser) {
        router.push('/admin');
    } else {
        router.push('/');
    }
  } catch (error) {
    console.error(error);
    errorMsg.value = '用户名或密码错误，请重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="card-header">
        <h2>欢迎回来</h2>
        <p>登录您的技术论坛账号</p>
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="请输入用户名"
            required 
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="请输入密码"
            required 
            :disabled="isLoading"
          />
        </div>
        
        <p v-if="successMsg" class="success-message">
          <span class="icon">✅</span> {{ successMsg }}
        </p>

        <p v-if="errorMsg" class="error-message">
          <span class="icon">⚠️</span> {{ errorMsg }}
        </p>
        
        <button type="submit" :class="{ 'loading': isLoading }" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '立即登录' }}
        </button>
      </form>
      
      <div class="card-footer">
        还没有账号？ <router-link to="/register">去注册一个</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 400px;
  transition: transform 0.3s ease;
}

/* 移动端适配 */
@media (max-width: 480px) {
  .login-wrapper {
    align-items: flex-start;
    padding-top: 3rem;
    background: #fff; /* 移动端可能更喜欢纯白背景 */
  }

  .login-card {
    box-shadow: none;
    padding: 1.5rem;
    border-radius: 0;
  }

  .card-header h2 {
    font-size: 1.5rem;
  }
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.card-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.card-header p {
  margin: 0.5rem 0 0;
  color: #7f8c8d;
  font-size: 0.95rem;
}

.success-message {
  color: #27ae60;
  background: #eafaf1;
  padding: 0.8rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #34495e;
  font-weight: 500;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box; /* 确保 padding 不会撑大宽度 */
}

input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

button {
  width: 100%;
  padding: 0.9rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
}

button:hover:not(:disabled) {
  background-color: #3aa876;
}

button:active:not(:disabled) {
  transform: scale(0.98);
}

button:disabled {
  background-color: #a8d5c2;
  cursor: not-allowed;
}

.error-message {
  background-color: #fff2f2;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.card-footer a {
  color: #42b983;
  text-decoration: none;
  font-weight: 600;
}

.card-footer a:hover {
  text-decoration: underline;
}
</style>
