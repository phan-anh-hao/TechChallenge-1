import { createApp } from 'vue'
import toast, { POSITION } from 'vue-toastification'
import type { PluginOptions } from 'vue-toastification'
import { createPinia } from 'pinia'
import 'vue-toastification/dist/index.css'
import 'ant-design-vue/dist/antd.css'

import App from './App.vue'
import router from './router'

const toastOptions: PluginOptions = {
  maxToasts: 4,
  position: POSITION.TOP_CENTER,
  timeout: 1900,
  hideProgressBar: true,
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(toast, toastOptions)

app.mount('#app')
