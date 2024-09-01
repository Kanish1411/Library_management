<template>
    <div v-if="$store.state.login">
        Hello
    </div>
  
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
export default {
    components:{
        Navbar,
    },
    data(){
        return{

        }
   },
   methods:{
        async checklogin(){
            const tk=localStorage.getItem("token");
            if (tk==null){
                this.$store.commit("setlogin",false);
                alert("Login to access this page");
                this.$router.push("/");
            }
            try{
            const resp=await axios.get("/checkLogin",{
            headers: {
            Authorization: "Bearer " + tk,
            },
            });
            console.log("askdhjoiad")
            if(resp.data.msg=="Valid"){
                this.$store.commit("setlogin",true);
            }   
            else{
                this.$store.commit("setlogin",false);
                alert("Login Required");
            }
        }
        catch{
            
        }
    }
   },
   created(){
    this.checklogin()
   },
}
</script>

<style>

</style>