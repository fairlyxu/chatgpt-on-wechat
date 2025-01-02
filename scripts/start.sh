#!/bin/bash

export BASE_DIR='/Users/feili.xu/Documents/99_workspace/boluo/chatgpt-on-wechat'
echo "base dir:""$BASE_DIR"

config_file=$1
echo ${BASE_DIR}/${config_file}

# 检查 nohup.out 日志输出文件是否存在
if [ ! -f "${BASE_DIR}/nohup.out" ]; then
  touch "${BASE_DIR}/nohup.out"
  echo "创建文件 ${BASE_DIR}/nohup.out"
fi

#python3 "${BASE_DIR}/assistan_start.py" --config_file="${BASE_DIR}/${config_file}"
python3 "${BASE_DIR}/assistan_start.py" --config_file="${BASE_DIR}/${config_file}"

# 启动 Python 脚本，并将输出追加到 nohup.out 文件中
#nohup python3 "${BASE_DIR}/assistan_start.py" --config_file="${BASE_DIR}/${config_file}" >> "${BASE_DIR}/nohup.out" 2>&1 &
#tail -f "${BASE_DIR}/nohup.out"

echo "Chat_on_webchat 正在启动，您可以检查 ${BASE_DIR}/nohup.out"
