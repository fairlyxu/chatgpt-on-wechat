#!/bin/bash

export BASE_DIR=`pwd`

config_file=$1
echo ${BASE_DIR}/${config_file}

# 获取今天的日期，格式为 YYYYMMDD
today=$(date +%Y%m%d)
log_file="${BASE_DIR}/logs/${today}_${config_file}.log"

# 检查 nohup.out 日志输出文件是否存在
if [ ! -f "${log_file}" ]; then
  touch "${log_file}"
  echo "创建文件 ${log_file}"
fi

# 启动 Python 脚本，并将输出追加到 nohup.out 文件中
nohup python3 "${BASE_DIR}/assistan_start.py" --config_file="${BASE_DIR}/${config_file}" >> "${log_file}" 2>&1 &tail -f "${log_file}"

echo "Chat_on_webchat 正在启动，您可以检查 ${log_file} 了解进程信息."
