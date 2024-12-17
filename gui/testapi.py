import tkinter
from tkinter import *
import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    root.title('群助手管理-登录')  # 程序的标题名称
    root.geometry("440x290+512+288")  # 窗口的大小及页面的显示位置
    root.resizable(False, False)  # 固定页面不可放大缩小
    root.iconbitmap("picture.ico")  # 程序的图标

    canvas = tkinter.Canvas(root, bg="white", height=400, width=700, borderwidth=-3)  # 创建画布
    from PIL import Image, ImageTk
    canvas.pack(side='top')  # 放置画布（为上端）
    # 打开图像并转换为tkinter可用的格式
    img = Image.open("/Users/feili.xu/Documents/99_workspace/boluo/chatgpt-on-wechat/test/11.jpg")
    image_file = ImageTk.PhotoImage(img)  # 使用ImageTk.PhotoImage来加载图片

    canvas.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上

    # 配置账户名
    var_usr_name = tkinter.StringVar()
    tkinter.Entry(root, width=16,borderwidth=0,textvariable=var_usr_name,font=('黑体', 16)).place(x=144,y=140)

    # 配置密码
    var_usr_pwd = tkinter.StringVar()
    tkinter.Entry(root, width=16, borderwidth=0,show='*', textvariable=var_usr_pwd, font=('黑体', 16)).place(x=144, y=184)

    # 错误提示
    def Tips():
        tkinter.Label(root, text='错误：账号或密码有误请重试！', bg="white", font=('宋体', 9), fg='red', width=60, borderwidth=2).place(
            x=30, y=220)

    # 登录
    def usr_login():
        usrs_info = ["张三","123456"]   # 账号与密码
        if usrs_info[0] == var_usr_name.get():   # 检测账号是否正确
            if usrs_info[1] == var_usr_pwd.get():   # 检测密码是否正确
                tkinter.messagebox.showinfo(title='登录', message='登录成功，欢迎使用！\n等待跳转！！！')  # 提示登录成功
            else:
                Tips()
        else:
            Tips()
    # 按钮
    Button(root, text='登录',bg='#ffffff',borderwidth=0.5, relief='ridge',width=32, font=('黑体', 13),command=usr_login).place(x=74,y=240)
    # text 按钮的文字显示
    # relief 边框的装饰     flat、raised、solid、ridge、groove
    # bg 按钮的背景色
    # fg 按钮的前景色
    # width 按钮的宽度   hright 按钮的高度
    # state 按钮的状态 normal、active、disabled  默认为normal
    # font 字体装饰  ("微软雅黑",10)  微软雅黑为字体名称，10为字体大小
    # command 按钮调用的函数
    # place 位置

    root.mainloop() #运行
if __name__ == '__main__':
    main()
