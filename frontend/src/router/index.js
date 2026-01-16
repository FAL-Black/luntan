import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import CreatePost from '../views/CreatePost.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/create-post', component: CreatePost },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
