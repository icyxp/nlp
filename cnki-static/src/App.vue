<template>
  <div id="app">
    <el-container >
      <el-header class="header">
        <div class="v5-header__logo">
          <a href="/">
              <img class="v5-header__img" src="./assets/logo_innosnap_100_w.png" alt="INNOVATION" />
          </a>
        </div>
      </el-header>

          <router-view></router-view>

      <!-- <el-footer>
        <p>Patsnap Hackathon 2018</p>
      </el-footer> -->
    </el-container>
  </div>
</template>

<script>
export default {
  methods: {
    
  }
}
</script>

<style>
body {
  margin: 0;
}
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
.el-header{
  height: 60px; 
  background-color: rgb(100, 177, 5);
}
.el-footer {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    text-align: center;
    color: #ccc;
}
.v5-header__logo {
    position: absolute;
    top: 11px;
    left: 20px;
    width: 100px;
    height: 30px;
}
</style>
