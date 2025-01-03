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


 // 禁用右键菜单
 document.addEventListener('contextmenu', function(event) {
  event.preventDefault();
});

// 额外处理：禁用F5刷新和地址栏刷新按钮（可选）
window.onbeforeunload = function() {
  return "你确定要离开这个页面吗？刷新或离开将丢失未保存的数据。";
};

// 禁用键盘上的 F5 和 Ctrl+R 刷新快捷键（可选，但可能需要更复杂的处理来完全阻止）
document.addEventListener('keydown', function(event) {
  if ((event.key === 'F5' || (event.ctrlKey && event.key === 'r')) && !event.shiftKey && !event.altKey && !event.metaKey) {
      event.preventDefault();
      return false;
  }
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
