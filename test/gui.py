import os
import tkinter as tk
from PIL import Image, ImageTk

# 设置字体
font = ("Arial", 12)


def create_input_row(frame, label_text, entry_variable, label_width=5, entry_width=20,):
    """创建一个输入行，包括标签和输入框"""
    label = tk.Label(frame, text=label_text, bg="white", width=label_width, anchor='w', font=font)  # 设置固定宽度
    entry = tk.Entry(frame, textvariable=entry_variable, width=entry_width, font=font)

    label.pack(side=tk.LEFT, padx=10)
    entry.pack(side=tk.LEFT, padx=10)



def create_login_window():
    global root, entry_username, entry_password, entry_tenant_id, entry_captcha, image_file
    root = tk.Tk()
    root.title("登录界面")
    root.geometry("400x280")

    # 设置窗口图标
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, 'src/icon.ico')
    print(icon_path)
    root.iconbitmap(icon_path)

    # 创建画布并设置背景图片
    canvas = tk.Canvas(root, bg="white", height=280, width=400)
    canvas.pack(side='top')

    # 加载并显示背景图片
    img = Image.open("/Users/feili.xu/Documents/99_workspace/boluo/chatgpt-on-wechat/test/11.jpg")
    image_file = ImageTk.PhotoImage(img)  # 确保保留对图像对象的引用
    canvas.create_image(0, 0, anchor='nw', image=image_file)

    # 创建输入框的容器
    input_frame = tk.Frame(root, bg="white")
    input_frame.place(relx=0.5, rely=0.5, anchor='center')  # 将输入框居中放置

    # 创建输入框
    entry_username = tk.StringVar()
    create_input_row(input_frame, "用户名", entry_username)
    input_frame.pack(pady=1)

    entry_password = tk.StringVar()
    create_input_row(input_frame, "密码", entry_password)
    input_frame.pack(pady=8)

    entry_tenant_id = tk.StringVar()
    create_input_row(input_frame, "租户ID", entry_tenant_id)
    input_frame.pack(pady=18)

    entry_captcha = tk.StringVar()
    create_input_row(input_frame, "验证码", entry_captcha)

    # 创建登录按钮
    login_button = tk.Button(root, text="登录",
                             command=lambda: print("登录信息：", entry_username.get(), entry_password.get()))
    login_button.place(relx=0.5, rely=0.85, anchor='center')  # 放置按钮在合适位置

    # 显示窗口
    root.mainloop()


# 调用函数以创建登录窗口
create_login_window()
