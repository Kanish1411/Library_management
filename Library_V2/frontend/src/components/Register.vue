<template>
  <div>
  <Navbar />
  <div class="container-color">
  <h1>Register</h1>
  <form @submit.prevent="register">
      <label for="username">Username:</label>
      <input class="form-control" type="text" v-model="username" required>
      <br>
      <label for="email">Email:</label>
      <input class="form-control" type="email" v-model="email" required>
      <br>
      <label  for="password">Password:</label>
      <input class="form-control" type="password" v-model="password" required>
      <br>
      <button class="btn btn-primary" type="submit">Register</button>
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
  name:"register",
  components:{
      Navbar,
  },
  data() {
  return {
      username: '',
      password: '',
      email:"",
      error: null,
      message: null,
    };

},
  methods:{
      async register(){
          try{
              const response = await axios.post('register', {
              username: this.username,
              password: this.password,
              email:this.email
              });
              const msg = response.data.message;
              if (msg=="registration Successful"){
                this.message=msg
              }
              else
                this.error=msg
          
          } catch (error) {
          console.log(error)
          this.error = 'Invalid details entered';
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