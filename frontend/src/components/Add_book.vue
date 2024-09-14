<template>
 <div v-if="$store.state.login && $store.state.lib "> 
    <Navbar libdash addsec/>
    <div class="container-color">
        <h2>Add  Book</h2>
        <br>
        <form @submit.prevent="submitBook">
            <label for="name">Book Name:</label>
            <input type="text" class="form-control" v-model="name" required>
            <label for="author">Author:</label>
            <input type="text" class="form-control" v-model="author" required>
            <label for="section">Select Section:</label>
            <select class="form-control" v-model="selectedSection" required>
                <option v-for="section in sections" :key="section.id" :value="section.id">
                    {{ section.name }}
                </option>
            </select>
            <label for="image">Upload Book Cover:</label>
            <input type="file"  class="form-control" @change="onFileChange('image', $event)" accept="image/*">
            <label for="content">Upload Book Content:</label>
            <input type="file" class="form-control" @change="onFileChange('content', $event)" accept=".txt,.pdf">
            <br>
            <button class="btn btn-primary" type="submit">Submit</button>
        </form>
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
            name: '',
            author: '',
            image: null,
            content: null,
            selectedSection: "",
            sections: []
        }
   },
   methods:{
    onFileChange(type, event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        if (type === 'image') {
          this.image = e.target.result.split(',')[1];
        } else if (type === 'content') {
          this.content = e.target.result.split(',')[1];
        }
      };
      reader.readAsDataURL(file);
    },
    fetchSections() {
            axios.get('/sections',{
              headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
              }
            }) .then(response => {
                    this.sections = response.data;
                })
                .catch(error => {
                    console.error('Error fetching sections:', error);
                });
        },
    submitBook() {
      const tk=localStorage.getItem("token");
      axios.post('/upload_book',{
        name: this.name,
        author: this.author,
        image: this.image,    
        content: this.content,
        section:this.selectedSection
      }, {
        headers: {
          Authorization:"Bearer "+tk,
        }
      })
      .then(response => {
        console.log('Book uploaded successfully:', response.data);
        this.$router.push("/librarian")
      })
      .catch(error => {
        console.error('Error uploading book:', error);
      });
    }
    },
   created(){
    checkLogin(this.$store, this.$router);
    checkLib(this.$store, this.$router);
    this.fetchSections();
},
}
</script>

<style>

</style>