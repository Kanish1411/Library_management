<template>
    <div>
    <Navbar userdash/>
    <div v-if="$store.state.login">
      <form  @submit.prevent="search">
        <label for="query">Search</label>
        <input class="form-control" v-model="query"  type="text">
        <button class="btn btn-primary" type="submit">Search</button>
      </form>
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
  </div>
  </template>
  
  <script>
  import Navbar from './Navbar.vue';
  import axios from 'axios';
  import { checkLogin } from '../auth';
  export default {  
      name:"Search",
      components:{
          Navbar
      },
      data(){
          return{
              sec:[],
              idu:0,
              query:""
          }
      },
      methods:{   
        async search(){
          const r=await axios.post("/search",{
            query:this.query
          })
          this.sec=r.data.l;
          console.log(this.sec);
        },
      },
      created(){
          checkLogin(this.$store, this.$router);
          this.idu=this.$route.params.id;
      },
  }
  </script>
  <style>
  </style>