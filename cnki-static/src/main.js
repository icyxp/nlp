import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'

import routes from './config/routes'

// import 'element-ui/lib/theme-chalk/index.css'
import '../theme/index.css'

import App from './App.vue'

Vue.use(ElementUI)
Vue.use(VueRouter)

const router = new VueRouter({
    routes
})

new Vue({
  el: '#app',
  render: h => h(App),
  router
})
