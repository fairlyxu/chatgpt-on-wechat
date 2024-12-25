<template>
    <el-container class="container is-vertical" style="height:100vh;">
        <el-container class="main-container">
            <el-aside width="200px" style="background-color: #545c64;">
                <el-menu  background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b"
                class="el-menu-vertical-demo" :default-active="defaultActive+''" @select="handleSelect">
                    <el-menu-item index="1">小助手设置</el-menu-item>
                    <el-menu-item index="2">系统设置</el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <el-form ref="assistForm" :model="assistFormData" class="assist-form">
                    <div id="menu1" v-show="activeIndex == 1">
                    
                        
                        <el-form-item prop="group_name_white_listStr"  label="群列表">
                            <el-input
                            v-model="assistFormData.group_name_white_listStr"
                            type="text"
                            auto-complete="off"
                            placeholder="群列表(请用逗号分割)">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="group_chat_in_one_sessionStr"  label="共享会话群列表">
                            <el-input
                            v-model="assistFormData.group_chat_in_one_sessionStr"
                            type="text"
                            auto-complete="off"
                            placeholder="共享会话群列表(请用逗号分割)">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="group_chat_prefixStr"  label="触发关键词">
                            <el-input
                            v-model="assistFormData.group_chat_prefixStr"
                            type="text"
                            auto-complete="off"
                            placeholder="触发关键词(请用逗号分割)">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="character_desc"  label="群助手角色描述">
                            <el-input
                            v-model="assistFormData.character_desc"
                            type="text"
                            auto-complete="off"
                            placeholder="群助手角色描述">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="subscribe_msg"  label="群助手功能描述">
                            <el-input
                            v-model="assistFormData.subscribe_msg"
                            type="text"
                            auto-complete="off"
                            placeholder="群助手功能描述">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="welcome_msg"  label="入群欢迎词">
                            <el-input
                            v-model="assistFormData.welcome_msg"
                            type="text"
                            auto-complete="off"
                            placeholder="入群欢迎词">
                        </el-input>
                        </el-form-item>
                    </div>
                    <div id="menu2" v-show="activeIndex == 2">
                        <el-form-item prop="group_msg_switch"  label="群消息管理">
                            <el-switch
                                v-model="assistFormData.group_msg_switch"
                                active-color="#13ce66">
                                </el-switch>
                        </el-form-item>
                    </div>
                </el-form>
            </el-main>
        </el-container>
        <div class="footer">
            <el-button :disabled="!running" type="danger" @click="stopRun" icon="el-icon-video-pause">停止</el-button>
            <el-button :disabled="startBtnDisabled || running" type="success" @click="startRun" icon="el-icon-video-play">启动</el-button>
            <!--<el-button type="danger" @click="toLoginPage" icon="el-icon-video-pause">退出登录</el-button>-->
        </div>
    </el-container>
   
</template>

<script>
import { getTenantId , getToken, storeGetUserInfo , storeLogOut  } from '@/store'
const tenantId = getTenantId()
var hasLoadConfig = false;
    export default {
        name:'Login',
        data(){
            return {
                defaultActive: 1,
                activeIndex: this.defaultActive,
                assistFormData:{
                    group_msg_switch:false
                }, //表单数据
                startBtnDisabled:true,//启动按钮是否禁用
                running:false,//是否已启动小助手
            }
        },
        methods:{
            toLoginPage(){
                window.pywebview.api.toLoginPage().then().catch(error=>{
                })
            },
            //验证token是否过期
            checkToken(){
                return new Promise((resolve, reject) => {
                     // 获取用户信息，验证token是否过期
                    storeGetUserInfo().then(res => {
                        resolve(res)
                    }).catch(error => {
                        reject(error)
                    })
                })
             
            },
            handleSelect(index, indexPath) {
                this.activeIndex = index
            },
            startRun(){//启动
                if(this.running){
                    this.$message.error('小助手已启动')
                    return
                }
                //启动之前判断token是否失效
                this.checkToken().then(()=>{
                    let formdata = {...this.assistFormData}
                    formdata.group_chat_prefix = formdata.group_chat_prefixStr ? formdata.group_chat_prefixStr.split(',') : []
                    formdata.group_name_white_list = formdata.group_name_white_listStr ? formdata.group_name_white_listStr.split(',') : []
                    formdata.group_chat_in_one_session = formdata.group_chat_in_one_sessionStr ? formdata.group_chat_in_one_sessionStr.split(',') : []
                    delete formdata.group_chat_prefixStr
                    delete formdata.group_name_white_listStr
                    delete formdata.group_chat_in_one_sessionStr
                    this.running = true
                    window.pywebview.api.startChat(formdata, tenantId,getToken()).then(response => {
                    }).catch(error=>{
                        this.running = false
                        this.$message.error("启动失败：" + error)
                    })
                }).catch(error=>{
                })
                
            },
            stopRun(){//停止
                window.pywebview.api.stopChat( tenantId).then(response => {           
                    this.$message.success("成功停止")
                    this.running = false
                    console.log("success响应",response)
                }).catch(error=>{
                    console.error(error)
                    this.$message.error(error)
                })
            },
            pywebviewReadyListener(){
                console.log("pywebviewReady")
                this.loadConfig()
            },
            //加载配置
            loadConfig(){
                if(hasLoadConfig){
                    return
                }
                try {
                    window.pywebview.api.loadConfig(tenantId).then(response => {
                        // if(response.code && response.code == 500){
                        //     alert(response.message)
                        //     document.getElementById('btn-generate').disabled = false
                        //     hideLoading()
                        //     return
                        // }
                        hasLoadConfig = true
                        let data = response.data
                        //数据格式化
                        data.group_chat_prefixStr = ""
                        if(data.group_chat_prefix){
                            data.group_chat_prefixStr = data.group_chat_prefix.join(",")
                        }
                        data.group_name_white_listStr = ""
                        if(data.group_name_white_list){
                            data.group_name_white_listStr = data.group_name_white_list.join(",")
                        }
                        data.group_chat_in_one_sessionStr = ""
                        if(data.group_chat_in_one_session){
                            data.group_chat_in_one_sessionStr = data.group_chat_in_one_session.join(",")
                        }
                        if(data.group_msg_switch == null || data.group_msg_switch == undefined){
                            data.group_msg_switch = false
                        }
                        this.assistFormData = data
                        this.startBtnDisabled = false
                        this.$message.success("加载配置成功")
                    }).catch(error=>{
                        console.error(error)
                        this.$message.error(error)
                        this.startBtnDisabled = true
                    })
                } catch (error) {
                    this.startBtnDisabled = true
                }
            },
        },
        created(){
            this.checkToken().then(()=>{
                window.addEventListener('pywebviewready', this.pywebviewReadyListener)
                this.handleSelect(this.defaultActive, '')
                this.loadConfig()
            }).catch(()=>{})
        },
        //页面卸载
        beforeDestroy(){
            window.removeEventListener('pywebviewready', this.pywebviewReadyListener)
        }
    }
</script>

<style scoped>
.container{
    padding:10px;
}
.main-container{
    height: calc(100vh - 100px);
}
.footer{
    text-align: right;
    padding-top: 20px;
    height:40px;
    padding-bottom:20px;
    border-top: 1px solid #eee;
}
</style>