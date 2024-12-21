import tab from './tab'
import cache from './cache'
import modal from './modal'

export default {
  install(Vue) {
    // 页签操作
    Vue.prototype.$tab = tab
    // 缓存对象
    Vue.prototype.$cache = cache
    // 模态框对象
    Vue.prototype.$modal = modal
  }
}
