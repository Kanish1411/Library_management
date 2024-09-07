<template>
    <div v-if="$store.state.login && $store.state.lib ">
        <Navbar addsec/>
        <div v-if="sec.length<1">
            <h4>No Sections Found </h4>
        </div>
        <div v-else>
            <div v-for="s in sec" :key="s.id">
                    <h5 class="container-color">
                    {{s.name}}<br>
                    {{ s.desc }}<br>
                    {{ s.date }}<br>
                    List of books:
                    </h5>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { checkLogin, checkLib } from '../auth';
export default {
    components:{
        Navbar,
    },
    data(){
        return{
            sec:[],
            books:[],
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
        this.books=resp.data.book;
    }
    catch (error){
        console.log(error);
    }
    },
   },
   created(){
    checkLogin(this.$store, this.$router);
    checkLib(this.$store, this.$router);
    this.fetch();
   },
}
</script>

<style>

</style>