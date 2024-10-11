<template>
  <div v-if="$store.state.login && $store.state.lib ">
    <Navbar libdash addbook/>
    <div class="container-color">
        <form @submit.prevent="Add_sec">
        <label for="name">Name:</label>
        <input class="form-control" type="text" v-model="name" required>
        <br>
        <label  for="Date">Date:</label>
        <input class="form-control" type="date" v-model="Date" value="Date" required>
        <label  for="Description">Description:</label>
        <textarea class="form-control" v-model="Description" required></textarea>
        <br>
        <button type="submit" class="btn btn-primary">Add</button>
    </form>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { checkLogin, checkLib } from '../auth';
export default {
    name:"Add Section",
    components:{
        Navbar,
    },
    data(){
        return{
            name:"",
            Date:new Date().toISOString().substr(0, 10), 
            Description:"",
        }
    },
    methods:{
        async Add_sec(){
            let tk=localStorage.getItem("token");
            const resp= await axios.post("/add_sec",{
                    name: this.name,
                    date:this.Date,
                    desc:this.Description
                },{
                    headers:{
                        Authorization:"Bearer "+tk
                    }})
            this.$router.push("/librarian")
        }
    },
    created(){
        checkLogin(this.$store, this.$router);
        checkLib(this.$store, this.$router);
    }
}
</script>

<style>

</style>