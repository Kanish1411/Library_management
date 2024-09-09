<template>
  <div>
    <div>
      <button @click="next" class="btn btn-primary">Next Page</button>
      <button @click="prev" class="btn btn-primary">Prev Page</button>
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

export default {
  data() {
    return {
      img: null, 
      pg: 0,
    };
  },
  methods: {
    async fetchBookPage(book_id, page_no) {
      try {
        const response = await axios.get(`/book/${book_id}/${page_no}`)
        console.log(response)
        if(response.data.error=="Invalid page number"){
          this.pg-=1;
          alert("the Book is over")
          response = await axios.get(`/book/${book_id}/${this.pg}`)
        }
        this.img = response.data.page_image;
      } catch (error) {
        console.error(error);
      }
    },
    next() {
      this.pg += 1;
      const book_id = this.$route.params.book_id;
      this.fetchBookPage(book_id, this.pg);
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
    this.fetchBookPage(book_id, this.pg); // Fetch the first page on load
  }
};
</script>

<style>
img {
  width: 60%;
  height: auto;
}
</style>
