import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Forgot_pwd from '@/components/Forgot_pwd.vue'
import Librarian from '@/components/Librarian.vue'
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
    },
    {
      name:"Forgot_pwd",
      component:Forgot_pwd,
      path:"/forgot"
    },
    {
      name:"Librarian",
      component:Librarian,
      path:"/librarian"
    }
  ]
})

export default router

