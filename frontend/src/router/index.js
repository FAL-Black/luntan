import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import CreatePost from '../views/CreatePost.vue';
import PostDetail from '../views/PostDetail.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/create-post', component: CreatePost },
  { path: '/post/:id', component: PostDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
