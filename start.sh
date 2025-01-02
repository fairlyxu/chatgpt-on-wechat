#!/bin/bash

# 查找并终止所有名为 assistan_start.py 的进程
pids=$(ps aux | grep '[a]ssistan_start.py' | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "没有找到正在运行的 assistan_start.py 进程。" | tee -a $LOG_FILE
else
    for pid in $pids; do
        kill -9 $pid  # 使用 SIGKILL (9) 强制终止进程
        echo "已终止进程 ID: $pid" | tee -a $LOG_FILE
    done
    echo "所有 assistan_start.py 进程已被终止。" | tee -a $LOG_FILE
fi



config_file=$1
echo ${BASE_DIR}/${config_file}

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
