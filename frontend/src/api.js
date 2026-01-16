import axios from 'axios';

// 创建 axios 实例，设置基础 URL
// 这里的 baseURL 会自动适配开发环境和生产环境（通过 Vite 代理）
const api = axios.create({
    baseURL: '/api',
    timeout: 5000,
});

// 请求拦截器：每次请求前，检查 localStorage 里有没有 token
// 如果有，就自动加到 headers 里面去
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器：如果后端返回 401 (未授权)，说明 token 过期或无效
// 自动清除本地 token，并强制跳转到登录页
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            // 这里简单处理，直接刷新页面或重定向
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export const getPosts = (skip = 0, limit = 100) => {
    return api.get(`/posts/?skip=${skip}&limit=${limit}`);
};

export const createPost = (postData) => {
    return api.post('/posts/', postData);
};

export const getPost = (postId) => {
    return api.get(`/posts/${postId}`);
};

export const getComments = (postId) => {
    return api.get(`/posts/${postId}/comments/`);
};

export const createComment = (postId, content) => {
    return api.post(`/posts/${postId}/comments/`, { content });
};

export default api;
