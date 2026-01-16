<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    // FastAPI 的 OAuth2PasswordRequestForm 需要 form data 格式
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);

    const res = await api.post('/token', formData);
    
    // 登录成功，保存 token
    localStorage.setItem('token', res.data.access_token);
    localStorage.setItem('username', username.value);
    
    // 跳转到首页
    router.push('/');
  } catch (error) {
    console.error(error);
    errorMsg.value = '登录失败，请检查用户名或密码';
  }
};
</script>

<template>
  <div class="auth-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>用户名</label>
        <input v-model="username" type="text" required />
      </div>
      <div class="form-group">
        <label>密码</label>
        <input v-model="password" type="password" required />
      </div>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <button type="submit">登录</button>
    </form>
    <p class="link">还没有账号？ <router-link to="/register">去注册</router-link></p>
  </div>
</template>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #3aa876;
}
.error {
  color: red;
  margin-bottom: 1rem;
}
.link {
  margin-top: 1rem;
  text-align: center;
}
</style>
