<template>
    <div v-if="$store.state.login && $store.state.lib ">
      <Navbar libdash addbook/>
      <div class="container-color">
          <form @submit.prevent="update_sec">
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
      name:"Update Section",
      components:{
          Navbar,
      },
      data(){
          return{
              name:"",
              Date:"", 
              Description:"",
          }
      },
      methods:{
          async update_sec(){
              let tk=localStorage.getItem("token");
              const resp= await axios.post("/update_sec",{
                      id:this.$route.params.id,
                      name: this.name,
                      date:this.Date,
                      desc:this.Description
                  },{
                      headers:{
                          Authorization:"Bearer "+tk
                      }})
              this.$router.push("/librarian")
          },
          async func(){
            const respo= await axios.get("/sections",{
                headers:{
                    Authorization: "Bearer "+ localStorage.getItem("token"),
                }
            })
            for(let i of respo.data){
                if (this.$route.params.id==i.id){
                    this.name=i.name;
                    this.Description=i.desc;
                    this.Date=i.date;
                }
            }  
        }
      }, 
      created(){
          checkLogin(this.$store, this.$router);
          checkLib(this.$store, this.$router);
          this.func()
        }
  }
  </script>
  
  <style>
  
  </style>