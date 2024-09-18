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
import Get_book from '@/components/Get_book.vue'
import Requests from '@/components/Requests.vue'
import My_books from '@/components/my_books.vue'
import Update_sec from '@/components/Update_sec.vue'
import Update_book from '@/components/Update_book.vue'
import Lendings from '@/components/Lendings.vue'
import Search from '@/components/Search.vue'


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
      path:"/book/:id/:book_id"
    },
    {
      name:"get_book",
      component:Get_book,
      path:"/get_book/:id/:book_id"
    },
    {
      name:"Requests",
      component:Requests,
      path:"/Requests"
    },
    {
      path:"/mybooks/:id",
      component:My_books
    },
    {
      path:"/update_sec/:id",
      component:Update_sec
    },
    {
      path:"/update_bk/:id",
      component:Update_book
    },
    {
      path:"/Lendings",
      component:Lendings
    },
    {
      path:"/search/:id",
      component:Search
    },
  ]
})

export default router

