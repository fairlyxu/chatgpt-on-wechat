# import wx
# app = wx.App()
import logging
import webview
import sys
import json
import subprocess
import os
import time
import signal
import assistan_start

# 获取当前工作目录
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


# current_file = __file__
# current_dir = os.path.dirname(os.path.abspath(current_file))

# 返回数据格式
#start_shell_script_path = f"{current_dir}/start_asistant.sh"
#stop_shell_script_path = f"{current_dir}/shutdown_asistant.sh"
#restart_shell_script_path = f"{current_dir}/restart_asistant.sh"

#script_name = f"{current_dir}/asistant_start.py"
start_shell_script_path = os.path.join(application_path,'start_asistant.sh')
stop_shell_script_path = os.path.join(application_path,"shutdown_asistant.sh")
restart_shell_script_path = os.path.join(application_path,"restart_asistant.sh")

script_name = os.path.join(application_path,"assistan_start.py")


def ApiResult(code, data, message):
    return {'data': data, 'code': code, 'message': message}

# 获取本项目的文件的绝对路径
def getAbsolueFilePath(filepath):
    return os.path.join(application_path,filepath)

class API:
    def __init__(self):
        self.config_file = ""
        self.process = None
        #self.script_name = os.path.join(application_path,"assistan_start.py")
        self.script_name = os.path.join(application_path,"assistant.exe")

    # 加载配置文件
    def loadConfig(self, tenantId):
        self.config_file = getAbsolueFilePath('config_' + tenantId + '.json')
        # 判断文件是否存在，如不存在，则加载config-template.json默认配置文件
        if not os.path.exists(self.config_file): 
            self.config_file = getAbsolueFilePath('config-template.json')
        if not os.path.exists(self.config_file):  # 如默认配置文件不存在，则报错
            raise Exception('配置文件不存在，且无默认配置文件')
        # utf-8格式读取文件内容
        with open(self.config_file, 'r', encoding='UTF-8') as f:
            data = json.load(f)
            return ApiResult(200, data, 'success')

    # 保存配置
    def saveConfig(self, configObj, tenantId, token):
        configObj["tenant_id"] = tenantId
        configObj["auth_token"] = token
        with open(getAbsolueFilePath('config_' + tenantId + '.json'), 'w', encoding='UTF-8') as f:
            # configObj 转成json字符串
            f.write(json.dumps(configObj))
        return ApiResult(200, True, 'success')

    def startChat(self, configObj="", tenantId="", token=""):
        if not self.is_running():
            # 调用saveConfig保存配置文件
            self.saveConfig(configObj, tenantId, token)
            filename = getAbsolueFilePath('config_' + tenantId + '.json')
            if not os.path.exists(filename):  # 如默认配置文件不存在，则报错
                raise Exception('配置文件不存在')
            print(f"Starting {self.script_name} with config file: {self.config_file}")
            args = [sys.executable, self.script_name]
            if self.config_file:
                args.append(self.config_file)
            self.process = subprocess.Popen(args)
            #assistan_start.run(self.config_file)
            print(f"{self.script_name} started with PID {self.process.pid}")

    def stopChat(self, tenantId):
        if self.is_running():
            print(f"Stopping {self.script_name}")
            self.process.send_signal(signal.SIGINT)  # 发送中断信号给子进程
            self.process.wait()  # 等待子进程结束
            print(f"{self.script_name} stopped")
            self.process = None

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def monitor(self):
        while True:
            if not self.is_running():
                print(f"{self.script_name} has stopped unexpectedly. Restarting...")
                self.startChat()
            time.sleep(5)  # 每隔5秒检查一次

    # 启动聊天助手
    def startChat_v0(self, configObj, tenantId, token):
        # 调用saveConfig保存配置文件
        self.saveConfig(configObj, tenantId, token)
        filename = getAbsolueFilePath('config_' + tenantId + '.json')
        if not os.path.exists(filename):  # 如默认配置文件不存在，则报错
            raise Exception('配置文件不存在')
        try:
            process = subprocess.Popen([start_shell_script_path, filename],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                logging.Logger("asistant_process 启动成功")
            else:
                logging.Logger("asistant_process 发生错误:", stderr.decode())
            return ApiResult(200, True, 'success')
        except Exception as e:
            raise Exception('启动失败，请检查配置文件是否正确')
        except subprocess.CalledProcessError as e:
            print(f"脚本执行失败，返回码: {e.returncode}")
            print("错误输出：", e.stderr)

    # 停止聊天助手
    def stopChatv0(self, tenantId):
        print("停止聊天助手")
        try:
            process = subprocess.Popen([stop_shell_script_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            self.is_running = False
            if process.returncode == 0:
                logging.Logger("asistant_process 启动成功")
            else:
                logging.Logger("asistant_process 发生错误:", stderr.decode())
            return ApiResult(200, True, '服务已停止')
        except Exception as e:
            return ApiResult(500, False, '停止服务失败: ' + str(e))

    def restart(self, tenantId):
        print("重启聊天助手")

    def toLoginPage(self):
        toLoginPage()


def toLoginPage():
    delete_cookie_and_reload("Admin-Token")


def delete_cookie_and_reload(cookie_name):
    # 替换为你要删除的 cookie 的名称
    if cookie_name is None or cookie_name == '':
        return
    # 执行 JavaScript 代码删除 cookie
    window.evaluate_js(f"document.cookie = '{cookie_name}=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';")
    # 刷新页面
    window.evaluate_js("location.reload();")

def main():
    api = API()
    

    # 1 页面还没打包时npm run build
    #url = 'http://localhost:8080' #开发时需要调页面代码时 使用： 必须在desktop_app下的desktop_vue_html 以 npm run serve命令启动vue项目后
    # 2 npm run build 已打包，加载打包后的html
    url = 'desktop_app/desktop_vue_html/dist/index.html?time=2'  # time=2用于清除上次的浏览器页面缓存
    url = os.path.join(application_path,url)
    global window
    window = webview.create_window('元芋智能 聊天小助手', url, width=700,height=700,  js_api=api)

    # private_mode=False 表示保存cookie,使其在app关掉重启后，依然保存cookie和本地存储
    webview.start(http_server=True,debug=True,private_mode=False) # 打开调试模式，开发时使用
   # webview.start(http_server=True,private_mode=False) # 关闭调试模式，生产环境时使用




