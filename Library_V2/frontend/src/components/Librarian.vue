<template>
    <div v-if="$store.state.login && $store.state.lib">
      <Navbar addsec addbook requests lend/>
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
              <p>Author: {{ b.author }}</p>
              <img 
                v-if="b.image" 
                :src="'data:image/jpeg;base64,' + b.image" 
                alt="Book Cover" 
                class="book-image"/>
              <div class="buttons">
                  <button class="btn btn-primary" @click="this.$router.push(`/update_bk/${b.id}`)">Update</button> <br>
                  <button class="btn btn-danger" @click="del(b.id)">Delete</button>
              </div> 
              <!-- <a 
                v-if="b.content" 
                :href="'data:application/pdf;base64,' + b.content" 
                download="book.pdf" 
                class="book-content-link">
                Request Download
              </a> -->
            </div>
          </div>
          <div v-else>
            No Books Found
          </div>
          <button class="btn btn-primary" @click="$router.push({ path: `/update_sec/${s.id}` })"> Update</button> {{ }}
          <button class="btn btn-danger" @click="delete_sec(s.id)"> Delete</button>
        </div>
      </div>
    </div>
  </template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { checkLogin, checkLib } from '../auth';
export default {
    components:{
        Navbar,
    },
    data(){
        return{
            sec:[],
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
    async del(id){
      if (window.confirm("Are you sure you want to delete this Book? (Leads to deletion of all Lendingfs and requests)")) {
      const tk = localStorage.getItem("token") 
      await axios.post("/delete_book",{
        id:id,
      },{
      headers:{
        Authorization:"Bearer "+tk,
      }})
      window.location.reload();
    }
    },
    delete_sec(id){
      if (window.confirm("Are you sure you want to delete this section? (Leads to deletion of all books in thius section)")) {
      axios.post("/delete_sec",{
        id:id
      },{
        headers:{
          Authorization:"Bearer "+localStorage.getItem("token"),
        }
      })
      window.location.reload();
    }
    },
   },
   created(){
    checkLogin(this.$store, this.$router);
    checkLib(this.$store, this.$router);
    this.fetch();
   },
}
</script>

<style>

</style>