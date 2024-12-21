import os  
from cryptography.fernet import Fernet  
import json
  
# 生成一个密钥（实际使用时，应将密钥硬编码在程序中，并安全地管理）  
# key = Fernet.generate_key()  
key = "trQIyapyyWU5mJ_nmKkLc6QxNEuxXts90ITX8lG6L00=" # key要硬编码

cipher_suite = Fernet(key)  
  
# 隐藏目录路径  
hidden_dir = os.path.join(os.path.expanduser("~"), ".yuanyuchatassistant")  
os.makedirs(hidden_dir, exist_ok=True)  
storage_file = os.path.join(hidden_dir, "storage.txt")  
  
# 加密和解密函数  
def encrypt_data(data):  
    if data == '':
        return ''
    return cipher_suite.encrypt(data.encode()).decode()  
  
def decrypt_data(encrypted_data):  
    if encrypted_data == '':
        return ''
    return cipher_suite.decrypt(encrypted_data.encode()).decode()  
  
# 根据key获取存储数据
def get_storage(key):
    storageData = _getAllStorage()  
    return storageData.get(key)

# 设置存储数据
def set_storage(key,value):
    storageData = _getAllStorage()
    storageData[key] = value
    with open(storage_file, 'w') as f:  
        f.write(encrypt_data(json.dumps(storageData)))  

def remove_storage(key):
    storageData = _getAllStorage()
    storageData.pop(key)
    with open(storage_file, 'w') as f:  
        f.write(encrypt_data(json.dumps(storageData)))
# 获取所有存储数据
def _getAllStorage():
    try:  
        # 读取激活状态  
        if os.path.exists(storage_file):  
            with open(storage_file, 'r') as f:  
                storageData = f.read()  
                storageData = decrypt_data(storageData)
                if storageData == "":
                    return {}
                return json.loads(storageData)
        else:
            return {}
    except FileNotFoundError:  
        return {}