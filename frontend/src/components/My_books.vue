<template>
  <div v-if="$store.state.login" >
    <div class="book" v-if="l.length > 0">
            <div v-for="b in l" :key="b.id" class="book-container">
              <h6>{{ b.name }}</h6>
              <p>Author(s): {{ b.author }}</p>
              <h6><strong>Time remaining:</strong>{{ b.timeleft }}</h6>
              <img v-if="b.image" :src="'data:image/jpeg;base64,' + b.image" alt="Book Cover"  class="book-image"/>
              <div class="buttons">
                <button class="btn btn-primary" @click="$router.push({ path: `/book/${this.idu}/${b.id}` })">Read</button><br>
                <button @click="RequestPDF" class="btn btn-primary">Request PDF</button>
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
export default {
    name:"My_books",
    data(){
      return{
        id:0,
        l:[],
      }
    },
    methods:{
        async fetch_books(){
          const resp=await axios.post("/mybooks",{
            id:this.id,
          })
            this.l=resp.data.l;
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