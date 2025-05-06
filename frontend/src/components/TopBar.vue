<script setup>
import { inject, ref, onMounted } from 'vue'
import axios from 'axios'
import { ui_config } from '@/config/config'
import { backend_config } from "@/config/system-config.js"

const userName = ref('')
const topBarColor = inject('topBarColor')

onMounted(async () => {
  try {
    const response = await axios.get(backend_config.backend_uri + '/get_current_user', {
      withCredentials: true
    })
    userName.value = response.data.name
  } catch (error) {
    // Silently handle error - user not logged in
  }
})
</script>

<template>
  <div class="topbar" :style="{ height: ui_config.top_bar_height, background: topBarColor }">
    <div class="left">
      <span>PC DPU</span>
    </div>
    <div class="right">
      <span v-if="userName">{{ userName }}</span>
    </div>
  </div>
</template>
  
  <style scoped>
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    background: #c40000;
    color: white;
    font-size: 1.2em;
    font-weight: 600;
  }
  
  .left {
    flex: 1;
    text-align: left;
  }
  
  .right {
    flex: 1;
    text-align: right;
  }
  </style>
  