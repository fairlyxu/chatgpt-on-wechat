import Vue from 'vue'
import Router from 'vue-router'
import { getToken } from '@/store'

Vue.use(Router)
// 公共路由
const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login'),
    hidden: true
  },
  {
    path: '/index',
    component: () => import('@/views/index'),
    hidden: true
  },
  {
    path: '/',
    redirect: '/index',
    hidden: true
  }
]

// 防止连续点击多次路由报错
let routerPush = Router.prototype.push;
let routerReplace = Router.prototype.replace;
// push
Router.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(err => err)
}
// replace
Router.prototype.replace = function push(location) {
  return routerReplace.call(this, location).catch(err => err)
}

//1. 创建router路由对象
const router =  new Router({
  mode: 'hash', // 保留url中的#
  base:process.env.VUE_APP_PUBLIC_BASE_PATH,
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

//2. 登录白名单
const whiteList = ['/login', '/register']
//3. 路由守卫
router.beforeEach((to, from, next) => {
  console.log('进入页面前 to from',to,from , getToken())
  if (getToken()) {
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next()
    }
  } else {
    // 没有token
    if (whiteList.indexOf(to.path) !== -1) {
      // 在免登录白名单，直接进入
      next()
    } else {
      next(`/login?redirect=${encodeURIComponent(to.fullPath)}`) // 否则全部重定向到登录页
    }
  }
})

export default router