<template>
    <div v-if="$store.state.login && $store.state.lib">
      <div class="container-color">
        <div class="row">
          <!-- Request Section -->
          <div class="col-md-6">
            <h3>Requests</h3>
            <div v-for="req in req_get" :key="req.id" class="request-item">
              <h5>{{req.name}} <br> {{ req.Book }} </h5>
              <button class="btn btn-success" @click="acceptRequest(req,req.id)">Accept</button>
              <button class="btn btn-danger" @click="rejectRequest(req,req.id)">Reject</button>
            </div>
          </div>
  
          <!-- PDF Section -->
          <div class="col-md-6">
            <h3>PDF Requests</h3>
            <div v-for="pdf in req_pdf" :key="pdf.id" class="pdf-item">
                <h5>{{pdf.name}} <br> {{ pdf.Book }} </h5>
              <button class="btn btn-success" @click="acceptRequest(pdf,pdf.id)">Accept</button>
              <button class="btn btn-danger" @click="rejectRequest(pdf,pdf.id)">Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Navbar from './Navbar.vue';
  import axios from 'axios';
  import { checkLogin, checkLib } from '../auth';
  
  export default {
    components: {
      Navbar,
    },
    data() {
      return {
        req_get: [],
        req_pdf: [],
      };
    },
    methods: {
      async fetch_req() {
        try {
          let tk = localStorage.getItem("token");
          const resp = await axios.get("/req_fetch", {
            headers: {
              Authorization: "Bearer " + tk,
            },
          });
          this.req_get = resp.data.Req_get;
          this.req_pdf = resp.data.Req_pdf;
          console.log(this.req_get, this.req_pdf);
        } catch (error) {
          console.log(error);
        }
      },
      acceptRequest(request,id) {
        console.log('Accepted:', id);
        const resp=axios.post("/acceptreq",{
            id:id,
            req:request,
        },{
            headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
            }
        })
        window.location.reload();
      },
      rejectRequest(request,id) {
        console.log('Rejected:', request);
        const resp=axios.post("/rejectreq",{
            id:id,
            req:request,
        },{
            headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
            }
        })
        window.location.reload();
        
      },
    },
    created() {
      checkLogin(this.$store, this.$router);
      checkLib(this.$store, this.$router);
      this.fetch_req();
    },
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 20px;
  }
  .request-item, .pdf-item {

    padding: 10px;
    margin-bottom: 15px;
    border-radius: 5px;
  }
  button {
    margin-right: 10px;
  }
  </style>
  