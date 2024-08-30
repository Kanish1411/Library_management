<template>
  <nav class="navbar navbar-expand-lg">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item active">
          <a class="nav-link active" href="/">Home</a>
        </li>
        <li class="nav-item active" v-if="register">
          <a class="nav-link active" href="/register">Register</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
</template>

<script>
export default {
    name:"Navbar",
    props:{
      register:{
        type:Boolean,
        default:false
      }
      
    },
}
</script>

<style>

</style>