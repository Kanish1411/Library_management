<template>
  <div v-if="$store.state.login">
    <Navbar mybook search/>
    <div class="container-color">
    <h3>
    {{ name }}
  </h3>
  <div v-if="l.length===0">
    No Books lended
  </div>
  <div v-else>
    <div v-for="b in l" :key="b.id" class="book-container">
              <h6>{{ b.name }}</h6>
              <p>Author(s): {{ b.author }}</p>
              <h6><strong>Time remaining:</strong>{{ b.time }}</h6>
              <img v-if="b.image" :src="'data:image/jpeg;base64,' + b.image" alt="Book Cover"  class="book-image"/>
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
            l:[],
            idu:0,
            name:""
        }
    },
    methods:{   
      async fetch(){
            try{
            let tk=localStorage.getItem("token");
            const resp=await axios.get(`/user_fetch/${this.idu}`,{
            headers:{
                Authorization:"Bearer "+tk,
                }
            })
            this.l=resp.data.l;
            this.name=resp.data.name;
      }
      catch (error){
          console.log(error);
      }
      },
    },
    created(){
        checkLogin(this.$store, this.$router);
        this.idu=this.$route.params.id;
        this.fetch();
        
    },
}
</script>
<style>
</style>