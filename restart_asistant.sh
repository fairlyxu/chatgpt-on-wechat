#!/bin/bash

config_file=$1
sh -x shutdown.sh

sh -x start.sh $1
echo "Chat_on_webchat 重启动，您可以检查 ${log_file} 了解进程信息."