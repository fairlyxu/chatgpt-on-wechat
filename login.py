# -*-coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import base64


import signal
import sys

from channel import channel_factory
from common.log import logger
from config import conf, load_config
from plugins import *
import argparse
from utils.APIconfig import LOGIN_URL,CAPTCHA_URL


captcha_image = None
captcha_tag = ""
login_url = LOGIN_URL
captcha_url = CAPTCHA_URL
from gui.login_gui import start_login

parser = argparse.ArgumentParser()

parser.add_argument('--config_file', type=str, help='配置文件目录', default="config.json")


def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def run(configfile=""):
    try:
        # load config
        load_config(configfile)
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"
            # os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:9001'

        channel = channel_factory.create_channel(channel_name)
        if channel_name in ["wx", "wxy", "terminal", "wechatmp", "wechatmp_service", "wechatcom_app", "wework"]:
            PluginManager().load_plugins()

        # startup channel
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)

# 配置类


# 全局变量存储验证码图像和验证码标识
captcha_image = None
captcha_tag = ""

# 获取验证码
def get_captcha():
    global captcha_image, captcha_tag
    response = requests.get(CAPTCHA_URL)
    if response.status_code == 200:
        data = response.json()['data']
        captcha_tag = data['tag']
        image_data = data['image']
        image_data = image_data.split(",")[1]  # 去掉前缀部分
        image_data = base64.b64decode(image_data)
        captcha_image = Image.open(io.BytesIO(image_data))
        captcha_image = captcha_image.resize((100, 40))  # 调整大小
        img = ImageTk.PhotoImage(captcha_image)
        label_captcha_img.config(image=img)
        label_captcha_img.image = img  # 保持引用
    else:
        messagebox.showerror("错误", "无法获取验证码！")

# 登录函数
def login(username, password, tenant_id, captcha_input):
    username = "admin"
    password = "123456"
    tenant_id = "1843853758772498438"
    global captcha_tag
    credentials = {
        "username": username,
        "password": password,
        "captchaCode": captcha_input,
        "captchaTag": captcha_tag
    }

    headers = {
        "Authorization": "Bearer test-token2",  # 替换为实际的Token
        "tenant-id": tenant_id
    }

    # 发送POST请求进行登录
    response = requests.post(LOGIN_URL, json=credentials, headers=headers)

    # 检查响应状态
    if response.status_code == 200:
        login_info = response.json()
        if login_info["code"] == 200:
            root.withdraw()  # 隐藏主窗口

            return True, f"欢迎, {username}!"  # 返回成功和消息
        else:
            get_captcha()  # 重新获取验证码
            return False, login_info["msg"]  # 返回失败信息
    else:
        get_captcha()  # 重新获取验证码
        return False, "登录请求失败！"  # 返回错误信息

# 居中窗口函数
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# 创建输入行
def create_input_row(label_text, entry_variable):
    frame = tk.Frame(root, bg="#f0f0f0")
    label = tk.Label(frame, text=label_text, bg="#f0f0f0", width=10, anchor='w')  # 设置固定宽度
    entry = tk.Entry(frame, textvariable=entry_variable, width=30)
    label.pack(side=tk.LEFT, padx=5)
    entry.pack(side=tk.LEFT, padx=5)
    frame.pack(pady=10)

# 创建验证码相关的行
def create_captcha_row():
    frame = tk.Frame(root, bg="#f0f0f0")
    label_captcha = tk.Label(frame, text="验证码：", bg="#f0f0f0", width=10, anchor='w')  # 设置固定宽度
    label_captcha.pack(side=tk.LEFT, padx=5)

    entry_captcha = tk.Entry(frame, width=15)
    entry_captcha.pack(side=tk.LEFT, padx=5)

    global label_captcha_img
    label_captcha_img = tk.Label(frame, bg="#f0f0f0")
    label_captcha_img.pack(side=tk.LEFT, padx=5)

    frame.pack(pady=10)
    return entry_captcha

# 封装登录窗口的创建
def create_login_window():
    global root, entry_username, entry_password, entry_tenant_id, entry_captcha

    root = tk.Tk()
    root.title("登录界面")
    root.configure(bg="#f0f0f0")
    root.geometry("400x300")

    # 创建输入框
    entry_username = tk.StringVar()
    create_input_row("用户名：", entry_username)
    entry_password = tk.StringVar()
    create_input_row("密码：", entry_password)
    entry_tenant_id = tk.StringVar()
    create_input_row("租户ID：", entry_tenant_id)

    # 创建验证码相关的行
    entry_captcha = create_captcha_row()

    # 创建登录按钮
    button_login = tk.Button(root, text="登录", command=lambda: handle_login(), bg="#4CAF50", fg="black")
    button_login.pack(pady=15)

    # 获取并显示验证码
    get_captcha()  # 初始获取验证码

    # 居中显示窗口
    center_window(root)

    # 运行主循环
    root.mainloop()

# 处理登录
def handle_login():
    global root
    username = entry_username.get()
    password = entry_password.get()
    tenant_id = entry_tenant_id.get()
    captcha_input = entry_captcha.get()

    success, message = login(username, password, tenant_id, captcha_input)

    if success:
        root.quit()  # 退出主循环
        root.destroy()
        run("../config_lama.json")
    else:
        messagebox.showerror("登录失败", message)

# 外部调用函数
def start_login():
    create_login_window()

if __name__ == '__main__':
    start_login()
