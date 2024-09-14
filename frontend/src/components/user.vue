<template>
  <div v-if="$store.state.login">
    <div v-if="sec.length === 0">
        <h4>No Sections Found</h4>
    </div>
    <div v-else>
        <div v-for="s in sec" :key="s.id" class="container-color">
          <h5 class="section-title">
            {{ s.name }}<br>
            {{ s.desc }}<br> 
          </h5>
          <div class="book" v-if="s.books.length > 0">
            <div v-for="b in s.books" :key="b.id" class="book-container">
              <h6>{{ b.name }}</h6>
              <p>Author(s): {{ b.author }}</p>
              <img v-if="b.image" :src="'data:image/jpeg;base64,' + b.image" alt="Book Cover"  class="book-image"/>
              <div class="buttons">
                <button class="btn btn-primary" @click="$router.push({ path:`/get_book/${this.idu}/${b.id}`})">GET</button><br>
              </div> 
            </div>
          </div>
          <div v-else>
            No Books Found
          </div>
          </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { checkLogin } from '../auth';
export default {  
    name:"user",
    components:{
        Navbar
    },
    data(){
        return{
            sec:[],
            idu:0,
        }
    },
    methods:{   
      async fetch(){
            try{
            let tk=localStorage.getItem("token");
            const resp=await axios.get("/Lib_fetch",{
            headers:{
                Authorization:"Bearer "+tk,
                }
            })
            this.sec=resp.data.Section;
      }
      catch (error){
          console.log(error);
      }
      },
      async RequestPDF(){
        console.log("jkadhakah")
      }
    },
    created(){
        checkLogin(this.$store, this.$router);
        this.fetch();
        this.idu=this.$route.params.id;
    },
}
</script>
<style>
</style>