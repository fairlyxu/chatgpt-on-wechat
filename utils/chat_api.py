# -*-coding:utf-8 -*-

"""
# File       : chat_api.py.py
# Time       ：2024/12/6 16:09
# Author     ：fairyxu 
# Description：
"""
import requests
import json
from .APIconfig  import UPLOAD_API
import signal

class ChatAPI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ChatAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self, tenant_id="1843853758772498438", auth_token="test-token2"):
        if not hasattr(self, 'initialized'):
            self.url = UPLOAD_API
            self.headers = {
                "tenant-id": tenant_id,
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }
            self.initialized = True

    def send_chat_record(self, chat_record):
        data = json.dumps(chat_record)
        response = requests.post(self.url, headers=self.headers, data=data)

        if response.status_code == 200:
            data = response.text
            json_data = json.loads(data)
            if json_data["code"] == 200:
                return response.json()
            else:
                signal.raise_signal(signal.SIGINT)
        else:
            raise Exception(f"请求失败: {response.status_code}, {response.text}")

# 全局实例
chat_api = ChatAPI()
