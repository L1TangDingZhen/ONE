import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import 'element-plus/theme-chalk/el-loading.css'
import 'element-plus/theme-chalk/el-message.css'


const app = createApp(App)

app.use(router)

app.mount('#app')

console.log('Base API URL:', process.env.VUE_APP_API_BASE_URL);
