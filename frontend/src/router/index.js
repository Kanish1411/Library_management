import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Forgot_pwd from '@/components/Forgot_pwd.vue'
import Librarian from '@/components/Librarian.vue'
import Admin from '@/components/Admin.vue'
import Add_section from '@/components/Add_section.vue'
import Add_book from '@/components/Add_book.vue'
import User from '@/components/user.vue'
import Read_book from '@/components/Read_book.vue'

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
    },
    {
      name:"User",
      component:User,
      path:"/user/:id"
    },
    {
      name:"Admin",
      component:Admin,
      path:"/admin"
    },
    {
      name:"Addsec",
      component:Add_section,
      path:"/addsec"
    },
    {
      name:"Addbook",
      component:Add_book,
      path:"/addbook"
    },
    {
      name:"readbook",
      component:Read_book,
      path:"/book/:book_id"
    }
  ]
})

export default router

