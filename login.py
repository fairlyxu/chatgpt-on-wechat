# -*-coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
import base64

import anyio
import signal
import sys
import json

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

options_dict = {
    "group_chat_prefix": "",
    "group_name_white_list": "",
    "group_chat_in_one_session": "",
    "character_desc": "",
    "subscribe_msg":"",
    "welcome_msg": ""
}
current_option = ''
text_area = None
login_window_start  =  False
def sigterm_handler_wrap(_signo):
    global login_window_start
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if login_window_start:
            print("登录窗口已启动")
        else:
            start_login()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        # sys.exit(0)


    signal.signal(_signo, func)
# run("../config_lama.json")
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
def create_input_row(label_text, entry_variable,label_width=10,entry_width=30):
    frame = tk.Frame(root, bg="#f0f0f0")
    label = tk.Label(frame, text=label_text, bg="#f0f0f0", width=label_width, anchor='w')  # 设置固定宽度
    entry = tk.Entry(frame, textvariable=entry_variable, width=entry_width)
    #entry = tk.Entry(frame, width=16, borderwidth=0, textvariable=entry_variable, font=('黑体', 16)).place(x=144, y=140)

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
    global root, entry_username, entry_password, entry_tenant_id, entry_captcha,login_window_start
    login_window_start = True

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
def show_text(option):
    global current_option
    current_option = option
    if option in options_dict:
        text_area.delete("1.0", tk.END)  # 清空文本域
        text_area.insert(tk.END, options_dict[option])  # 插入对应的文本内容
    else:
        messagebox.showwarning("警告", "未找到对应的选项内容！")

def on_text_change(event):
    global text_area
    global options_dict
    if current_option:
        options_dict[current_option] = text_area.get("1.0", "end-1c")

def init_config():
    global options_dict
     # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件的完整路径

    config_path = os.path.join(script_dir,  'config_lama.json')

    try:
        config_str = ''
        # 打开并读取配置文件
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config_str = config_file.read()
        config = json.loads(config_str)
        if config :
            options_dict["group_chat_prefix"] = config.get("group_chat_prefix", "")[0]
            options_dict["group_name_white_list"] =",".join(config.get("group_name_white_list", "")) 
            options_dict["group_chat_in_one_session"] =",".join(config.get("group_chat_in_one_session", ""))  
            options_dict["character_desc"] = config.get("character_desc", "")
            options_dict["subscribe_msg"] = config.get("subscribe_msg", "")
            options_dict["welcome_msg"] = config.get("welcome_msg", "")

        return True

    except FileNotFoundError:
        print(f"配置文件未找到: {config_path}")
        messagebox.showwarning("警告", "配置文件未找到！")
        return False

    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")
        messagebox.showwarning("警告", "配置文件解析错误！")
        return False

    except Exception as e:
        print(f"发生了一个错误: {e}")
        return False


def confirm_config():
    global root
     # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件的完整路径

    config_path = os.path.join(script_dir,  'config_lama.json')

    try:
        config_str = ''
        # 打开并读取配置文件
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config_str = config_file.read()
        config = json.loads(config_str)
        config["group_chat_prefix"][0] = options_dict["group_chat_prefix"]
        #将options_dict["group_name_white_list"]中的中文逗号转换为英文逗号
        options_dict["group_name_white_list"] = options_dict["group_name_white_list"].replace("，", ",")
        config["group_name_white_list"] =[item for item in options_dict["group_name_white_list"].split(",") if item.strip()] 
        options_dict["group_chat_in_one_session"] = options_dict["group_chat_in_one_session"].replace("，", ",")
        config["group_chat_in_one_session"] =  [item for item in options_dict["group_chat_in_one_session"].split(",") if item.strip()]
        config["character_desc"] = options_dict["character_desc"]
        config["subscribe_msg"] = options_dict["subscribe_msg"]
        config["welcome_msg"] = options_dict["welcome_msg"]
        #写回配置文件
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)
        root.quit()  # 退出主循环
        root.destroy()
        run("config_lama.json")

        # run("../config_lama.json")
    except FileNotFoundError:
        print(f"配置文件未找到: {config_path}")
        messagebox.showwarning("警告", "配置文件未找到！")

    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")
        messagebox.showwarning("警告", "配置文件解析错误！")

    except Exception as e:
        print(f"发生了一个错误: {e}")
    except KeyboardInterrupt:
        print("用户已中断")
        

def create_config_window():
    global text_area
    global root
    init_config()
    root = tk.Tk()
    root.title("配置界面")
    root.geometry("600x500")

    # 创建一个主框架用于容纳所有控件，这样可以更好地控制布局
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建左侧的 Treeview 控件（代替 Listbox）
    options_tree = ttk.Treeview(main_frame, selectmode='browse', height=10)
    options_tree["columns"] = ("one",)  # 定义一列
    options_tree.column("#0", width=0, stretch=tk.NO)  # 隐藏默认的树状结构列
    options_tree.column("one", anchor="w", width=200)  # 设置列宽和对齐方式

    # 设置列标题作为标签行
    options_tree.heading("one", text="配置选项", anchor="w")  # "选项" 是列标题

    options_tree.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # 将选项添加到 Treeview 中，仅显示 key 并指定 iid 以确保唯一性
    for idx, option in enumerate(options_dict.keys(), start=1):
        options_tree.insert("", "end", iid=str(idx), values=(option,))

    text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=20)
    text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_area.bind("<Double-1>", lambda event: None)  # 禁用双击事件
    text_area.bind("<KeyRelease>", on_text_change)
    # 绑定 Treeview 的选择事件
    options_tree.bind("<<TreeviewSelect>>", lambda event: show_text(options_tree.item(options_tree.selection())['values'][0]))

    # 创建一个框架用于容纳按钮，并将其放置在窗口底部
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # 创建按钮并将其放置在框架中央
    login_button = tk.Button(button_frame, text="启动", command=confirm_config)
    login_button.pack(pady=10, side=tk.BOTTOM)  # 使用 pady 提供额外的空间，side=tk.BOTTOM 确保按钮在框架底部

    center_window(root)

    # 运行主循环
    root.mainloop()

# 处理登录
def handle_login():
    global root,login_window_start
    username = entry_username.get()
    password = entry_password.get()
    tenant_id = entry_tenant_id.get()
    captcha_input = entry_captcha.get()

    success, message = login(username, password, tenant_id, captcha_input)

    if success:
        root.quit()  # 退出主循环
        root.destroy()
        login_window_start = False
        create_config_window()
        #run("../config_lama.json")
    else:
        messagebox.showerror("登录失败", message)
# 外部调用函数
def start_login():
    create_login_window()

from utils.chat_api import ChatAPI

if __name__ == '__main__':
    start_login()

    # sigterm_handler_wrap(signal.SIGINT)
    # chatapi = ChatAPI()
    # record = {"message":"nihao"}
    # chatapi.send_chat_record(record)