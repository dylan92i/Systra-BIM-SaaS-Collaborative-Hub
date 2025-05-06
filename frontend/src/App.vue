<template>
  <div id="app">
    <router-view class="login-fullscreen" />
  </div>
</template>

<script setup>
// Pas besoin d'importer un composant ici !
</script>

<style>
html, body, #app {
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.login-fullscreen {
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
}
</style>
