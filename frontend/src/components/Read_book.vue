<template>
  <div>
    <Navbar />
    <div class="page_header">
    <div class="page">
      <button @click="prev" class="btn btn-primary">Prev Page</button>
      {{   }}
      <button @click="next" class="btn btn-primary">Next Page</button>
    </div>
    <div class="pgno">
      <b>
      {{pg+1}}/{{ total}}
    </b>
    </div>
  </div>
    <div class="img-holder" v-if="img">
      <img :src="'data:image/png;base64,'+ img" class="responsive-image"/>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "./Navbar.vue";
export default {
  data() {
    return {
      img: null, 
      pg: 0,
      total:1,
    };
  },
  components:{
  Navbar,
  },
  methods: {
    async fetchBookPage(book_id, page_no) {
      try {
        let response = await axios.get(`/book/${book_id}/${page_no}`)
        if(response.data.error=="Invalid page number"){
          this.pg-=1
          response = await axios.get(`/book/${book_id}/${this.pg-1}`)
        }
        else{
        this.img = response.data.page_image;
        this.total=response.data.page_no;
        }
      } catch (error) {
        console.error(error);
      }
    },
    next() {
    if(this.pg<this.total){
      this.pg += 1;
      const book_id = this.$route.params.book_id;
      this.fetchBookPage(book_id, this.pg);
    }
    },
    prev() {
      this.pg -= 1;
      if(this.pg<0){
        this.pg=0; 
      }
      else{
      const book_id = this.$route.params.book_id;
      this.fetchBookPage(book_id, this.pg);
      }
    }
  },
  mounted() {
    const book_id = this.$route.params.book_id;
    this.fetchBookPage(book_id, this.pg);
  }
};
</script>
<style>
.page_header{
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;
}
.pgno{
  margin: 10px;
  padding :2px;
  background-color: #00000027;
  border-radius: 10px;
}
</style>