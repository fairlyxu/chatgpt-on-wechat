# -*-coding:utf-8 -*-

"""
# File       : login.py
# Time       ：2024/12/9 14:30
# Author     ：fairyxu
# Description：
"""

import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io
import base64
from utils.APIconfig import LOGIN_API,CAPTCHA_API

# 全局变量存储验证码图像和验证码标识
captcha_image = None
captcha_tag = ""
login_url = LOGIN_API
captcha_url = CAPTCHA_API

# 获取验证码
def get_captcha():
    global captcha_image, captcha_tag
    response = requests.get(captcha_url)
    if response.status_code == 200:
        data = response.json()['data']
        captcha_tag = data['tag']
        image_data = data['image']
        image_data = image_data.split(",")[1]
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
    global captcha_tag,login_res
    # 用户的登录凭据
    credentials = {
        "username": username,
        "password": password,
        "captchaCode": captcha_input,  # 用户输入的验证码
        "captchaTag": captcha_tag  # 验证码标识
    }

    # 添加请求头
    headers = {
        "Authorization": "Bearer test-token2",  # 替换为实际的Token
        "tenant-id": tenant_id  # 使用用户输入的租户ID
    }

    # 发送POST请求进行登录
    response = requests.post(login_url, json=credentials, headers=headers)
    msg = ""
    # 检查响应状态
    if response.status_code == 200:
        login_info = response.json()
        msg = login_info["msg"]
        title = "登录成功"
        if login_info["code"] == 200:
            root.withdraw()
            msg = f"欢迎, {username}!"
            login_res = "True"
        else:
            title = "登录失败"
            get_captcha()
        messagebox.showinfo(title, msg)
    else:
        messagebox.showerror("错误", "登录请求失败！")
        get_captcha()  # 重新获取验证码

    return login_res

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
    global root, entry_username, entry_password, entry_tenant_id, entry_captcha,login_res

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
    button_login = tk.Button(root, text="登录", command=lambda: login(entry_username.get(), entry_password.get(), entry_tenant_id.get(), entry_captcha.get()), bg="#4CAF50", fg="black")
    button_login.pack(pady=15)

    # 获取并显示验证码
    get_captcha()  # 初始获取验证码

    # 居中显示窗口
    center_window(root)

    # 运行主循环
    root.mainloop()


# 外部调用函数
def start_login():
    create_login_window()


if __name__ == '__main__':
    start_login()
