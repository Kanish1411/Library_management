<template>
  <div>
    <Navbar />
    <div v-if="a==true">
        <div class="container-color">
            <form @submit.prevent="email_check">
                <label for="email">Enter email for Recovery:</label>
                <input class="form-control" type="text" v-model="email" required><br>
                <button class="btn btn-primary" type="submit">Get OTP</button>
            </form>
        </div>
    </div>
    <div v-if="a==false & b==false">
        <div class="container-color">
            <form @submit.prevent="otp_check">
                <label for="otp">Enter OTP:</label>
                <input class="form-control" type="text" v-model="otp" maxlength="6" minlength="6" required><br>
                <button class="btn btn-primary" type="submit">Change Password</button>
            </form>
        </div>
    </div>
    <div v-if="a==false & b==true">
        <div class="container-color">
            <form @submit.prevent="change_pwd">
                <label for="otp">Enter New Password:</label>
                <input class="form-control" type="text" v-model="pwd" required><br>
                <label for="otp">Retype Password:</label>
                <input class="form-control" type="text" v-model="pwd2" required><br>
                <button class="btn btn-primary" type="submit">Change Password</button>
            </form>
        </div>
    </div>
    <div v-if="err" class="message error-message"><b>{{ err }}</b></div>
    <div v-if="msg" class="message success-message">{{ msg }}</div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
import crypto from 'crypto-js';

export default {
  components: { Navbar },
    name:"Forgot_pwd",
    components:{
        Navbar,
    },
    data(){
        return{
            a:true,
            email:"",
            msg:"",
            err:"",
            otp:"",
            timeoutId: null,
            hash:"",
            b:false,
            pwd:"",
            pwd2:"",
        }
    },
    methods: {
        async email_check(){
            try{
            const respo=await  axios.post("/forgot_pwd",{
                email:this.email
            })
            const resp=respo.data.msg;
            this.hash=respo.data.hash;
            if(resp=="Email Not found"){
                this.err="Email Not found";
            }
            else{
                this.msg=resp;
                this.a=false;
            }
            this.resetMessages(); 
        }
        catch (error){
            this.error = 'Invalid credentials';
            this.resetMessages(); 
        }
        },
        async otp_check() {
            const hotp = crypto.SHA256(this.otp).toString();
            console.log(this.otp);
            
            if(hotp==this.hash){
                this.b=true;
            }
            else{
                this.err="wrong OTP!!!!!!!!!!!"
                this.resetMessages(); 
            }
        },
        async change_pwd(){
            if(this.pwd!=this.pwd2){
                this.err="Password must match";
                this.resetMessages(); 
            }
            else{
                const resp=await axios.post("/change_pwd",{
                    email:this.email,
                    pwd:this.pwd,
                })
                this.msg=resp.data.msg
                setTimeout(()=>{
                    this.$router.push("/")
                },2000)
            }
        },
        resetMessages() {
            if (this.timeoutId) {
                clearTimeout(this.timeoutId);
            }
            this.timeoutId = setTimeout(() => {
                this.msg = null;
                this.err = null;
            }, 3000);
        }   
    }
}
</script>
<style>
</style>