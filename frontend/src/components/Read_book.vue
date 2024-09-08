<template>
    <div>
      <iframe v-if="bookContent"
        :src="'data:application/pdf;base64,' + bookContent+'#toolbar=0'"
        width="60%"
      ></iframe>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        bookContent: null,
      };
    },
    methods: {
      async fetchBook(book_id) {
        try {
          const response = await axios.get(`/book/${book_id}`);
          this.bookContent = response.data.book_content;
        } catch (error) {
          console.error(error);
        }
      },
    },
    mounted() {
      const book_id = this.$route.params.book_id;
      this.fetchBook(book_id);
    },
  };
  </script>
  <style>


iframe {
  width: 60%;
  height: 100vh;
}
</style>
  