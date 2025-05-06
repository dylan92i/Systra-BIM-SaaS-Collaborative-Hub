import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n from './languages/i18n.js'
import Vue3Lottie from 'vue3-lottie'

const app = createApp(App)

app.use(router)
app.use(i18n)
app.use(Vue3Lottie);

app.mount('#app')

