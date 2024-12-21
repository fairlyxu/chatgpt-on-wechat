<template>
    <div class="login">
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form">
        <h3 class="title">{{ APP_TITLE }}</h3>
        <el-form-item prop="tenantId"  label="租户ID">
            <el-input
            v-model="loginForm.tenantId"
            type="text"
            auto-complete="off"
            placeholder="租户ID"
            prefix-icon="el-icon-user-solid"
          >
          </el-input>
        </el-form-item>
        <el-form-item prop="username" label="账号">
          <el-input
            v-model="loginForm.username"
            type="text"
            auto-complete="off"
            placeholder="账号"
            prefix-icon="el-icon-user-solid"
          >
          </el-input>
        </el-form-item>
        <el-form-item prop="password" label="密码">
          <el-input
            v-model="loginForm.password"
            type="password"
            auto-complete="off"
            placeholder="密码"
            @keyup.enter.native="handleLogin"
            prefix-icon="el-icon-lock"
          >
          </el-input>
        </el-form-item>
        <el-form-item prop="captchaCode" v-if="captchaEnabled">
          <el-input
            v-model="loginForm.captchaCode"
            auto-complete="off"
            placeholder="验证码"
            style="width: 63%"
            @keyup.enter.native="handleLogin"
          >
            <svg-icon slot="prefix" icon-class="validCode" class="el-input__icon input-icon" />
          </el-input>
          <div class="login-code">
            <img :src="codeUrl" @click="getCode" class="login-code-img"/>
          </div>
        </el-form-item>
  
        <el-checkbox v-model="loginForm.rememberMe" style="margin:0px 0px 25px 0px;">记住密码</el-checkbox>
        <el-form-item style="width:100%;">
          <el-button
            :loading="loading"
            size="medium"
            type="primary"
            style="width:100%;"
            @click.native.prevent="handleLogin"
          >
            <span v-if="!loading">登 录</span>
            <span v-else>登 录 中...</span>
          </el-button>
          <div style="float: right;" v-if="register">
            <router-link class="link-type" :to="'/register'">立即注册</router-link>
          </div>
        </el-form-item>
      </el-form>
      <!--  底部  -->
      <!-- <div class="el-login-footer">
        <span>Copyright © 2018-2025 fisher.vip All Rights Reserved.</span>
      </div> -->
    </div>
  </template>
  
  <script>
  import { getCodeImg } from "@/api/login";
  import Cookies from "js-cookie";
  import { encrypt, decrypt } from '@/utils/jsencrypt'
  import { storeLogOut ,storeLogin,setTenantId , removeTenantId, storeGetUserInfo } from '@/store'
  
  export default {
    name: "Login",
    data() {
      return {
        APP_TITLE:process.env.VUE_APP_TITLE,
        codeUrl: "",
        loginForm: {
          username: "",
          password: "",
          rememberMe: false,
          captchaCode: "",//验证码
          captchaTag: "" //验证码的tag唯一标识符
        },
        loginRules: {
          username: [
            { required: true, trigger: "blur", message: "请输入您的账号" }
          ],
          password: [
            { required: true, trigger: "blur", message: "请输入您的密码" }
          ],
          captchaCode: [{ required: true, trigger: "change", message: "请输入验证码" }],
          tenantId:[
            { required: true, trigger: "blur", message: "请填写租户ID" }
          ]
        },
        loading: false,
        // 验证码开关
        captchaEnabled: process.env.VUE_APP_CAPTCHA_ENABLED == undefined ? true : process.env.VUE_APP_CAPTCHA_ENABLED,
        // 注册开关
        register: false,
        redirect: undefined,
      };
    },
    watch: {
      $route: {
        handler: function(route) {
          this.redirect = route.query && route.query.redirect;
        },
        immediate: true
      }
    },
    created() {
      this.getCode();
      this.getCookie();
    },
    methods: {
      getCode() {
        getCodeImg().then(res => {
          if (this.captchaEnabled) {
            this.codeUrl = res.data.image;
            this.loginForm.captchaTag = res.data.tag;
          }
        }).catch(error=>{

        });
      },
      getCookie() {
        const tenantId = Cookies.get("tenantId");
        const username = Cookies.get("username");
        const password = Cookies.get("password");
        const rememberMe = Cookies.get('rememberMe')
        this.loginForm = {
          tenantId: tenantId === undefined ? this.loginForm.tenantId : tenantId,
          username: username === undefined ? this.loginForm.username : username,
          password: password === undefined ? this.loginForm.password : decrypt(password),
          rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
        };
      },
      handleLogin() {
        this.$refs.loginForm.validate(valid => {
          if (valid) {
            setTenantId(this.loginForm.tenantId)
            this.loading = true;
            if (this.loginForm.rememberMe) {
              Cookies.set("tenantId", this.loginForm.tenantId, { expires: 30 });
              Cookies.set("username", this.loginForm.username, { expires: 30 });
              Cookies.set("password", encrypt(this.loginForm.password), { expires: 30 });
              Cookies.set('rememberMe', this.loginForm.rememberMe, { expires: 30 });
            } else {
              Cookies.remove("tenantId");
              Cookies.remove("username");
              Cookies.remove("password");
              Cookies.remove('rememberMe');
            }
            storeLogin(this.loginForm).then((token) => {
              // 获取用户信息
              storeGetUserInfo().then(res => {
                this.$router.push({ path: this.redirect || "/" }).catch(()=>{});
              }).catch(error => {
                //获取用户信息失败，则退出登录
                storeLogOut().then(() => {
                  this.$router.push(`/login?redirect=${this.$route.fullPath}`);
                });
              })

            }).catch(() => {
              //删除tenantId
              removeTenantId();
              this.loading = false;
              if (this.captchaEnabled) {
                this.getCode();
              }
            });
          }
        });
      },
    }
  };
  </script>
  
  <style rel="stylesheet/scss">
  .login {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* background-image: url("../assets/images/login-background.jpg"); */
    background-size: cover;
    background-color: #eee;
  }
  .title {
    margin: 0px auto 30px auto;
    text-align: center;
    color: #707070;
  }
  
  .login-form {
    border-radius: 6px;
    background: #ffffff;
    width: 400px;
    padding: 25px 25px 5px 25px;
    
  }
.login-form .el-input {
    height: 38px;
    input {
      height: 38px;
    }
  }
  .login-form .input-icon {
    height: 39px;
    width: 14px;
    margin-left: 2px;
  }
  .login-tip {
    font-size: 13px;
    text-align: center;
    color: #bfbfbf;
  }
  .login-code {
    width: 33%;
    height: 38px;
    float: right;
    
  }
  .login-code  img {
      cursor: pointer;
      vertical-align: middle;
    }
  .el-login-footer {
    height: 40px;
    line-height: 40px;
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: #fff;
    font-family: Arial;
    font-size: 12px;
    letter-spacing: 1px;
  }
  .login-code-img {
    height: 45px;
  }
  
  @media screen and (max-width: 400px){
    .login-form{
      width:100%;
      margin-left:20px;
      margin-right: 20px;
    }
  }
  </style>
  