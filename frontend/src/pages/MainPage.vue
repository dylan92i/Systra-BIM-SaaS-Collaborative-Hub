<template>
  <div class="app">
    <Loading v-if="showLoading" />
    <template v-else>
      <TopBar v-if="showTopBar" />
      <div class="main-content">
        <SideBar />
        <div class="content-area">
          <router-view /> <!-- Le contenu dépend de la sous-route -->
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'
import TopBar from '@/components/TopBar.vue'
import SideBar from '@/components/SideBar.vue'
import Loading from '@/components/Loading.vue'

const showLoading = ref(true)
onMounted(() => {
  const min = 2, max = 3
  const delay = Math.random() * (max - min) + min
  setTimeout(() => {
    showLoading.value = false
  }, delay * 1000)
})

// ---- Show/hide TopBar ----
const showTopBar = ref(true) 
const topBarColor = ref('#c40000') 

provide('showTopBar', showTopBar)
provide('topBarColor', topBarColor)
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.content-area {
  flex: 1;
  background-color: white;
  overflow: auto;
}
</style>
