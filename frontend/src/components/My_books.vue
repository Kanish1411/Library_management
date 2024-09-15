<template>
  <div v-if="$store.state.login" >
    sdjfoilsjfiopj90hlkbtujnhjk[spdflij0sfjlioy8]
  </div>
</template>

<script>
 import { checkLogin } from '../auth';
 import axios from 'axios';
export default {
    name:"My_books",
    methods:{
        async fetch_books(){
              
        }
    },  
    created(){
    checkLogin(this.$store, this.$router);
    },
}
</script>

<style>

</style>