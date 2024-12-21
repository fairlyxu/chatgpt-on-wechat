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
                    
                        <el-form-item prop="group_chat_prefixStr"  label="群列表(请用逗号分割)">
                            <el-input
                            v-model="assistFormData.group_chat_prefixStr"
                            type="text"
                            auto-complete="off"
                            placeholder="群列表(请用逗号分割)">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="group_name_white_listStr"  label="共享会话群列表">
                            <el-input
                            v-model="assistFormData.group_name_white_listStr"
                            type="text"
                            auto-complete="off"
                            placeholder="共享会话群列表">
                        </el-input>
                        </el-form-item>
                        <el-form-item prop="group_chat_in_one_session"  label="触发关键词">
                            <el-input
                            v-model="assistFormData.group_chat_in_one_session"
                            type="text"
                            auto-complete="off"
                            placeholder="触发关键词">
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
        </div>
    </el-container>
   
</template>

<script>
import { getTenantId } from '@/store'
const tenantId = getTenantId()
var hasLoadConfig = false;
    export default {
        name:'Login',
        data(){
            return {
                defaultActive: 1,
                activeIndex: this.defaultActive,
                assistFormData:{}, //表单数据
                startBtnDisabled:true,//启动按钮是否禁用
                running:false,//是否已启动小助手
            }
        },
        methods:{
            handleSelect(index, indexPath) {
                this.activeIndex = index
            },
            startRun(){//启动
                if(this.running){
                    this.$message.error('小助手已启动')
                    return
                }
                window.pywebview.api.startChat(this.assistFormData, tenantId).then(response => {
                    this.running = true
                    this.$message.success("启动成功")
                }).catch(error=>{
                    console.error(error)
                    this.$message.error(error)
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
                        this.assistFormData = response.data
                        //数据格式化
                        this.assistFormData.group_chat_prefixStr = ""
                        if(this.assistFormData.group_chat_prefix){
                            this.assistFormData.group_chat_prefixStr = this.assistFormData.group_chat_prefix.join(",")
                        }
                        this.assistFormData.group_name_white_listStr = ""
                        if(this.assistFormData.group_name_white_list){
                            this.assistFormData.group_name_white_listStr = this.assistFormData.group_name_white_list.join(",")
                        }
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
            console.log('created')
            window.addEventListener('pywebviewready', this.pywebviewReadyListener)
            this.handleSelect(this.defaultActive, '')
            this.loadConfig()
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