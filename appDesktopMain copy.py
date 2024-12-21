# import wx
# app = wx.App()
import webview
import os
import sys
from app import run # 聊天小助手
import json
from desktop_app.storage import get_storage,set_storage,remove_storage

# 当前电脑用户目录
USERPATH = os.path.expanduser('~')
# 当前电脑下载目录
DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'),'Downloads','数迈科技-聊天小助手')
# 创建默认保存目录
if not os.path.exists(DEFAULT_DOWNLOAD_PATH):
    os.makedirs(DEFAULT_DOWNLOAD_PATH)

# 返回数据格式

def ApiResult(code,data,message):
    return {'data':data,'code':code,'message':message}

class API:
    # def say_hello(self, name):
    #     time.sleep(2)  # 模拟一个耗时操作
    #     return f'Hello, {name}!'
    def getStorage(self,key):
        return get_storage(key)

    def login(self,tenantId,token):
        set_storage("tenantId",tenantId)
        set_storage("token",token)
        set_storage("isLogin",True)

    def loginOut(self):
        set_storage("isLogin",False)
        remove_storage("tenantId")
        remove_storage("token")

    # 加载配置文件
    def loadConfig(self,tenantId):
        filename = 'config_' + tenantId + '.json'
        # 判断文件是否存在，如不存在，则加载config-template.json默认配置文件
        if not os.path.exists(filename):
            filename = 'config-template.json'
        if not os.path.exists(filename):# 如默认配置文件不存在，则报错
            raise Exception('配置文件不存在，且无默认配置文件')
        # utf-8格式读取文件内容
        with open(filename, 'r',encoding='UTF-8') as f:
            data = json.load(f)
            return ApiResult(200, data, 'success')

    # 保存配置
    def saveConfig(self,configObj,tenantId):
        with open('config_' + tenantId + '.json', 'w',encoding='UTF-8') as f:
            # configObj 转成json字符串
            f.write(json.dumps(configObj))
        return ApiResult(200, True, 'success')

    # 启动聊天助手
    def startChat(self,configObj,tenantId):
        # 调用saveConfig保存配置文件
        self.saveConfig(configObj,tenantId)
        filename = 'config_' + tenantId + '.json'
        if not os.path.exists(filename):# 如默认配置文件不存在，则报错
            raise Exception('配置文件不存在')
        # app.run(filename)
    
    # 停止聊天助手
    def stopChat(self,tenantId):
        pass

#def set_cookies(window):
#    # 定义设置 Cookie 的 JavaScript 代码
#    cookies = ''
#    tenantId = get_storage("tenantId")
#    token = get_storage("token")
#    if tenantId is not None and tenantId != '':
#        cookies += "document.cookie = 'TenantId=" + tenantId+"';"
#    if token is not None and token != '':
#        cookies += "document.cookie = 'Admin-Token=" + token+"';"
#    if cookies != '':
#        set_cookie_js = "(function() {" + cookies +"})();"
#        window.evaluate_js(set_cookie_js)

def main():
    api = API()
    # # 获取当前工作目录  
    # if getattr(sys, 'frozen', False):
    #     # If the application is run as a bundle, the PyInstaller bootloader
    #     # extends the sys module by a flag frozen=True and sets the app 
    #     # path into variable _MEIPASS'.
    #     application_path = sys._MEIPASS
    # else:
    #     application_path = os.path.dirname(os.path.abspath(__file__))

    # url = 'public/login.html' # 打开网址，若没有激活，则跳转到登录页面。若激活则跳转到首页
    # if check_activation_status():
    #     url = 'public/index.html'
    # url = 'public/index.html'
    # webview.create_window('数迈科技 文本转语音', os.path.join(application_path,url), width=900,height=830,  js_api=api)
    # webview.start(http_server=True) # 不打开调试模式，打包时用这个
    url = 'http://localhost:8080/index'
    window = webview.create_window('数迈科技 聊天小助手', url, width=700,height=500,  js_api=api)
    # private_mode=False 表示保存cookie,使其在app关掉重启后，依然保存cookie和本地存储
    webview.start(http_server=True,debug=True,private_mode=False) # 打开调试模式，开发时使用
    #webview.start(set_cookies,window,http_server=True,debug=True,private_mode=False) # 打开调试模式，开发时使用
    
