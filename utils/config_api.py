# -*-coding:utf-8 -*-

"""
# File       : config_api.py
# Time       ：2024/12/9 19:06
# Author     ：fairyxu 
# Description：
"""
import requests
from .APIconfig import CONFIG_URL

test_json= {
  "open_ai_api_key": "YOUR API KEY",
  "model": "boluo",
  "channel_type": "wx",
  "proxy": "",
  "hot_reload": True,
  "single_chat_prefix": [
    ""
  ],
  "single_chat_reply_prefix": "",
  "group_chat_prefix": [
    ""
  ],
  "group_name_white_list": [
    "量子位AI交流群 23群",
    "水瓶座和她的朋友们",
    "辣妈好物分享①",
     "Micro Saas开发者工会1群",
    "春田妇儿22年全国7-9月辣妈群"

  ],
  "group_chat_in_one_session": [
     "量子位AI交流群 23群",
    "水瓶座和她的朋友们",
    "辣妈好物分享①",
     "Micro Saas开发者工会1群",
    "春田妇儿22年全国7-9月辣妈群"
  ],
  "image_create_prefix": [
    "画",
    "看",
    "找"
  ],
  "speech_recognition": False,
  "group_speech_recognition": False,
  "voice_reply_voice": False,
  "conversation_max_tokens": 1000,
  "expires_in_seconds": 3600,
  "character_desc": "你是辣妈AI小助理。优质母婴群助理，帮妈妈们解决育儿问题，欢迎调戏，嘻嘻。每次回答请尽量简短精干。每次回答控制在150字数以内",
  "subscribe_msg": "感谢您的关注！\n这里是辣妈姐妹淘，可以自由对话。 ",
  "welcome_msg": "\n\n\n【辅食工具合集】 为你精心挑选，路过就来看看吧\uD83D\uDC49\uD83D\uDC49\uD83D\uDC49#小程序://快团团/点击跟团/NaOBJe1iWztJ64h \n【辅食合集】 为你精心挑选，路过就来看看吧\uD83D\uDC49\uD83D\uDC49\uD83D\uDC49#小程序://快团团/点击跟团/DlXqJz6tvHrs3pg \n【成长保健品合集】 为你精心挑选，路过就来看看吧\uD83D\uDC49\uD83D\uDC49\uD83D\uDC49#小程序://快团团/点击跟团/nZQKVE4kECbzi4k \n【待产集合】 为你精心挑选，路过就来看看吧\uD83D\uDC49\uD83D\uDC49\uD83D\uDC49#小程序://快团团/点击跟团/06kAYE0o5E5783F\n",
  "use_linkai": False,
  "linkai_api_key": "",
  "linkai_app_code": ""
}

class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False  # 标记初始化状态
        return cls._instance

    def __init__(self, config_url):
        if self._initialized:  # 避免重复初始化
            return

        self.config_url = config_url
        self.data = self.load_config()  # 加载配置
        self._initialized = True

    def load_config(self):
        try:
            #response = requests.get(CONFIG_URL)
            #response.raise_for_status()  # 检查请求是否成功
            response = requests.post(self.url, headers=self.headers, data=json.dumps(chat_record))
            if response.status_code == 200:
                return response.json()
                return response.json()  # 返回 JSON 数据
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return {}
        except ValueError:
            print("解码 JSON 时出错")
            return {}

    def update_config(self):
        """重新加载配置数据"""
        self.data = self.load_config()



# 全局实例
config_api = Config()