<template>
    <div>
    <Navbar register/>
    <div class="container-color">
    <h1>Login</h1>
    <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input class="form-control" type="text" v-model="username" required>
        <br>
        <label  for="password">Password:</label>
        <input class="form-control" type="password" v-model="password" required>
        <br>
        <a href="/forgot">Forgot Password?</a>
        <br>
        <button class="btn btn-primary" type="submit">Login</button>
      </form>
      <div v-if="error" class="message error-message"><b>{{ error }}</b></div>
      <div v-if="message" class="message success-message">{{ message }}</div>
    </div>
    </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
    name:"login",
    components:{
        Navbar,
    },
    data() {
    return {
        username: '',
        password: '',
        error: null,
        message: null,
      };

  },
    methods:{
        async login(){
            try{
                const response = await axios.post('login', {
                    username: this.username,
                    password: this.password,
                });
                const msg = response.data.message;
                this.$store.commit("setlogin",true);
                if(msg=="Admin Login"){
                    localStorage.setItem("token",response.data.token);
                }
                else if(msg=="Librarian Login"){
                    console.log("Librarian");
                    localStorage.setItem("token",response.data.token);
                    
                }
                else if(msg=="User Login"){
                    console.log("user");
                    localStorage.setItem("token",response.data.token);
                }   
                else
                    this.error=msg;
            } catch (error) {
            console.log(error)
            this.error = 'Invalid credentials';
        }
        setTimeout(() => {
            this.message = null;
            this.error = null;
        }, 3000);
        }

    }
}
</script>

<style>

</style>