import Cookies from 'js-cookie'
import { login, logout, getInfo } from '@/api/login'

const TokenKey = 'Admin-Token'

const IsLoginKey = 'isLogin'

const userInfoKey = "UserInfo"

const tenantIdKey = "TenantId"

const cookieExpires = 30

export function storeLogOut(){
  return new Promise((resolve, reject) => {
    logout(state.token).then(() => {
      setIsLogin(false);
      removeTenantId();
      removeToken()
      resolve()
    }).catch(error => {
      reject(error)
    })
  })
}

export function storeLogin(userInfo){
    // 将用户信息存在本地存储中
    const username = userInfo.username.trim()
    const password = userInfo.password
    const captchaCode = userInfo.captchaCode
    const captchaTag = userInfo.captchaTag
    return new Promise((resolve, reject) => {
      login(username, password, captchaCode, captchaTag).then(res => {
        let token = res.data.tokenValue;
        setToken(token)
        setIsLogin(true)
        resolve(token)
      }).catch(error => {
        reject(error)
      })
    })
}

export function storeGetUserInfo(){
  return new Promise((resolve, reject) => {
    getInfo().then(res => {
      const user = res.data
      // const avatar = (user.avatar == "" || user.avatar == null) ? require("@/assets/images/profile.jpg") : process.env.VUE_APP_BASE_API + user.avatar;
      const avatar = (user.avatar == "" || user.avatar == null) ? require("@/assets/images/profile.jpg") : user.avatar;
      user.avatar = avatar
      setUserInfo(user)
      setTenantId(user.tenantId)
      resolve(res)
    }).catch(error => {
      reject(error)
    })
  })
}

export function getTenantId() {
  return Cookies.get(tenantIdKey)
}

export function setTenantId(tenantId) {
  return Cookies.set(tenantIdKey, tenantId,{ expires: cookieExpires})
}

export function removeTenantId() {
  return Cookies.remove(tenantIdKey)
}


export function getToken() {
  let tmp = Cookies.get(TokenKey)
  return tmp
}

export function setToken(token) {
  return Cookies.set(TokenKey, token,{ expires: cookieExpires})
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function getIsLogin() {
    return !!Cookies.get(IsLoginKey)
  }
  
  export function setIsLogin(isLogin) {
    return Cookies.set(IsLoginKey, !!isLogin,{ expires: cookieExpires})
  }
  
  export function removeIsLogin() {
    return Cookies.remove(IsLoginKey)
  }

  export function getUserInfo() {
    return Cookies.get(userInfoKey) ? JSON.parse(Cookies.get(userInfoKey)) : null
  }
  
  export function setUserInfo(userInfo) {
    return Cookies.set(userInfoKey, JSON.stringify(userInfo),{ expires: cookieExpires})
  }
  
  export function removeUserInfo() {
    return Cookies.remove(userInfoKey)
  }