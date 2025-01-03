#!/bin/bash


# 查找并终止所有名为 assistan_start.py 的进程
pids=$(ps aux | grep 'assistan_start.py' | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "没有找到正在运行的 assistan_start.py 进程。" | tee -a $LOG_FILE
else
    for pid in $pids; do
        kill -9 $pid  # 使用 SIGKILL (9) 强制终止进程
        echo "已终止进程 ID: $pid" | tee -a $LOG_FILE
    done
    echo "所有 assistan_start.py 进程已被终止。" | tee -a $LOG_FILE
fi

