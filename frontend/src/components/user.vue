<template>
  <div v-if="$store.state.login">
    <div v-if="sec.length === 0">
        <h4>No Sections Found</h4>
      </div>
      <div v-else>
        <div v-for="s in sec" :key="s.id" class="container-color">
          <h5 class="section-title">
            {{ s.name }}            {{ s.date }}<br>
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
                  <button class="btn btn-primary">Read</button> <br>
              </div> 
              <a
                v-if="b.content" 
                :href="'data:application/pdf;base64,' + b.content" 
                :download= "b.name+'.pdf'"
                class="book-content-link">
                Request Download
              </a>
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
import { checkLogin, checkLib } from '../auth';
export default {
    name:"user",
    components:{
        Navbar
    },
    data(){
        return{
            sec:[]
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
    },
    created(){
        checkLogin(this.$store, this.$router);
        this.fetch();
    },
}
</script>

<style>

</style>