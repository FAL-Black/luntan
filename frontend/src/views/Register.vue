<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const username = ref('');
const email = ref('');
const password = ref('');
const errorMsg = ref('');
const router = useRouter();

const handleRegister = async () => {
  try {
    await api.post('/register', {
      username: username.value,
      email: email.value,
      password: password.value
    });
    
    alert('注册成功！请登录');
    router.push('/login');
  } catch (error) {
    console.error(error);
    if (error.response && error.response.data) {
        errorMsg.value = error.response.data.detail || '注册失败';
    } else {
        errorMsg.value = '注册失败，请稍后重试';
    }
  }
};
</script>

<template>
  <div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>用户名</label>
        <input v-model="username" type="text" required />
      </div>
      <div class="form-group">
        <label>邮箱</label>
        <input v-model="email" type="email" required />
      </div>
      <div class="form-group">
        <label>密码</label>
        <input v-model="password" type="password" required />
      </div>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <button type="submit">注册</button>
    </form>
    <p class="link">已有账号？ <router-link to="/login">去登录</router-link></p>
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
