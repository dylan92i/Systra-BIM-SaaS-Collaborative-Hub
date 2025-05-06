<template>
    <div class="lottie-bg">
      <Vue3Lottie :animationData="AstronautJSON" :height="350" :width="350" />
    </div>
  </template>
  
  <script setup>
  import { Vue3Lottie } from 'vue3-lottie'
  import AstronautJSON from '@/assets/loading_animation.json'
  </script>
  
  <style scoped>
  .lottie-bg {
    min-height: 100vh;            /* Prend toute la hauteur de la fenêtre */
    display: flex;
    justify-content: center;      /* Centre horizontalement */
    align-items: center;          /* Centre verticalement */
    background: rgb(190, 199, 208);;             /* Gris clair */
  }
  </style>