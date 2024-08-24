import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name:"Login",
      component:Login,
      path:"/"
    }

  ]
})

export default router

