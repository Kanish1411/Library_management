<template>
<div>
  <Navbar chart />
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
import { checkLogin, checkAd } from '../auth';
import axios from 'axios';
export default {
    name:"Admin",
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
        
    },
    created(){
    checkLogin(this.$store, this.$router);
    checkAd(this.$store, this.$router);
    this.fetch();
   },
}
</script>

<style>

</style>