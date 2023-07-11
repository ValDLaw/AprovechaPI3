import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index'; // Ruta correcta a tu archivo de store Vuex

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta : {requiresAuth: true}
  },
  {
    path: '/register',
    name: 'Registro',
    component: () => import('../views/Register.vue')
  },{
    path: "/venta",
    name : "Venta",
    component: () => import("../views/Venta.vue"),
    meta : {requiresAuth: true},
    props : true
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    console.log(store.getters.isAuthenticatedExists); 
    if (store.getters.isAuthenticatedExists) {
      next();
      return;
    }
    next("/login");
  } else {
    next();
  }
});

export default router
