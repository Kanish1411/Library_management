import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name:"Login",
      component:Login,
      path:"/"
    },
    {
      name:"Register",
      component:Register,
      path:"/register"
    }

  ]
})

export default router

