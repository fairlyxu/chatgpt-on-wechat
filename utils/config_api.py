# -*-coding:utf-8 -*-

"""
# File       : config_api.py
# Time       ：2024/12/9 19:06
# Author     ：fairyxu 
# Description：
"""
import requests
from .APIconfig import CONFIG_URL


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
            response = requests.get(CONFIG_URL)
            response.raise_for_status()  # 检查请求是否成功
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