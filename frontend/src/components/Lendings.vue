<template>
    <div v-if="$store.state.login && $store.state.lib">
        <Navbar libdash/>
        <div v-if="l">
            <div v-for="i in l" :key="i.id" class="book-container">
                Username {{ i.name }}<br>
                Book {{ i.bk_name }}<br>
                {{ i.time }}<br>
                <button class="btn btn-danger" @click="revoke(i.id)">Revoke</button>
            </div>
        </div>
        <div v-else>
            No Lendings Yet
        </div>
    </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { checkLogin, checkLib } from '../auth';
export default {
    name:"Lendings",
    data(){
        return{
            l:[]
        }
    },
    components:{
        Navbar,
    },
    methods:{
        async fetch_lend(){
            const resp=await axios.get("/fetch_l",{
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token"),
                }
            })
            console.log(resp)
            this.l=resp.data.l;
        },
        revoke(id){
            axios.put("/revoke",{
                id:id
            },{
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token")
                }
            })
            window.location.reload();
        }
    },
    created(){
          checkLogin(this.$store, this.$router);
          checkLib(this.$store, this.$router);
          this.fetch_lend();
    }

}
</script>

<style>

</style>