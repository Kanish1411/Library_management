<template>
    <div >
      <Navbar userdash />
      <div v-if="book.length>0">
              <!-- <h6>{{ b.name }}</h6>
              <p>Author(s): {{ b.author }}</p> -->
              <img v-if="book[0].image" :src="'data:image/jpeg;base64,' + book[0].image" alt="Book Cover"  class="read-book-image"/>
              <div class="buttons-1">
                <h4> Book name: {{ book[0].name }}</h4>
                <h5> Authors: {{ book[0].author  }}</h5>
                <button class="btn btn-primary" @click="$router.push({ path: `/book/${this.idu}/${book[0].id}` })">Read</button><br>
                <button @click="get_book" class="btn btn-primary">Get Book for 7 days</button><br>
                <button @click="RequestPDF" class="btn btn-primary">Request PDF</button>
            </div>
        </div>
        <div v-if="error" class="message error-message"><b>{{ error }}</b></div>
      <div v-if="message" class="message success-message">{{ message }}</div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import Navbar from "./Navbar.vue";
  export default {
    data() {
      return {
        idu:0,
        book_id:0,
        book:[],
        error: null,
        message: null,
      };
    },
    components:{
    Navbar,
    },
    methods: {
        async fetch_bk_det(){
            const tk=localStorage.getItem("token");
            try{
            const resp= await axios.post("/fetch_bk_det",{
                bk_id:this.book_id,
            },{
                headers:{
                    Authorization:"Bearer "+tk,
                }
            })
            this.book=resp.data.book;
            console.log(this.book)
        }
        catch (err){
            console.log(err)
        }
        },
        async RequestPDF(){
            const tk=localStorage.getItem("token");
            const resp= await axios.post("/request_book",{
                bk_id:this.book_id,
                id:this.idu,
            },{
                headers:{
                    Authorization:"Bearer "+tk,
                }
            })

        this.message=resp.data.msg;
        this.error=resp.data.err;
        setTimeout(() => {
            this.message = null;
            this.error = null;
        }, 3000);
    },
    async get_book(){
            const resp= await axios.post("/get_book",{
                bk_id:this.book_id,
                id:this.idu,
            },{
                headers:{
                    Authorization:"Bearer "+localStorage.getItem("token"),
                }
            })
            this.message=resp.data.msg;
            this.error=resp.data.err;
            setTimeout(() => {
            this.message = null;
            this.error = null;
        }, 3000);
    }
    },

    created() {
      this.book_id = this.$route.params.book_id;
      this.idu=this.$route.params.id;
      this.fetch_bk_det();
    }
  };
  </script>
  <style>
  .read-book-image{
    margin: 35px auto;
    bottom: 10px;
    display: flex;
    flex-direction: column;
    padding: 5px;
    max-width: 400px;         
    max-height: 500px;
  }
  .buttons-1{
    margin:auto;
    bottom: 10px;
    display: flex;
    flex-direction: column;
    padding: 5px;
    max-width: 20%;
}

  </style>