<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const username = ref('');
const email = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const router = useRouter();

const handleRegister = async () => {
  errorMsg.value = '';
  isLoading.value = true;
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
    if (error.response) {
        // 后端返回的错误
        if (error.response.status === 422) {
             errorMsg.value = '参数格式错误，请检查输入';
        } else if (error.response.data && error.response.data.detail) {
            errorMsg.value = error.response.data.detail;
        } else {
            errorMsg.value = `服务器错误 (${error.response.status})`;
        }
    } else if (error.request) {
        // 请求发不出去（网络问题或后端没起）
        errorMsg.value = '无法连接到服务器，请检查网络或联系管理员';
    } else {
        errorMsg.value = '注册发生未知错误';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="register-wrapper">
    <div class="register-card">
      <div class="card-header">
        <h2>创建账号</h2>
        <p>加入我们的技术社区</p>
      </div>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="给自己起个好听的名字"
            required 
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label>电子邮箱</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="example@email.com"
            required 
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="设置您的登录密码"
            required 
            :disabled="isLoading"
          />
        </div>
        
        <p v-if="errorMsg" class="error-message">
          <span class="icon">⚠️</span> {{ errorMsg }}
        </p>
        
        <button type="submit" :class="{ 'loading': isLoading }" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '立即注册' }}
        </button>
      </form>
      
      <div class="card-footer">
        已有账号？ <router-link to="/login">直接登录</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 1rem;
}

.register-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 400px;
  transition: transform 0.3s ease;
}

.register-card:hover {
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
  box-sizing: border-box;
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
