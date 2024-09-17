<template>
  <div v-if="$store.state.login" >
    <Navbar userdash/>
    <div class="book" v-if="l.length > 0">
            <div v-for="b in l" :key="b.id" class="book-container">
              <h6>{{ b.name }}</h6>
              <p>Author(s): {{ b.author }}</p>
              <h6><strong>Time remaining:</strong>{{ b.timeleft }}</h6>
              <img v-if="b.image" :src="'data:image/jpeg;base64,' + b.image" alt="Book Cover"  class="book-image"/>
              <div class="buttons">
                <button class="btn btn-primary" @click="$router.push({ path: `/book/${this.id}/${b.id}` })">Read</button><br>
                <button @click="RequestPDF(b.id)" class="btn btn-primary">Request PDF</button>
                <br>
                <button class="btn btn-primary" @click="ret_bk(b.id)">Return</button>
              </div> 
            </div>
          </div>
          <div v-else>
            No Books Found
      </div>
  </div>
</template>

<script>
 import { checkLogin } from '../auth';
 import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
    name:"My_books",
    data(){
      return{
        id:0,
        l:[],
      }
    },
    components:{
      Navbar
    },
    methods:{
        async fetch_books(){
          const resp=await axios.post("/mybooks",{
            id:this.id,
          })
            this.l=resp.data.l;
        },
        RequestPDF(book_id){
            const tk=localStorage.getItem("token");
            const resp= axios.post("/request_book",{
                bk_id:book_id,
                id:this.id,
            },{
                headers:{
                    Authorization:"Bearer "+tk,
                }
            })
          },
          ret_bk(id){
            const resp= axios.post("/return_bk",{
                bk_id:id,
            },{
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token"),
                }
            })
            window.location.reload();
          }
    },  
    created(){
    this.id = this.$route.params.id;
    checkLogin(this.$store, this.$router);
    this.fetch_books();
    },
}
</script>

<style>

</style>