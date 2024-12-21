import Vue from 'vue'
import Cookies from 'js-cookie'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import './assets/icons' // icon
Vue.use(ElementUI, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})

Vue.config.productionTip = false

console.log("再main.js文件中")

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
