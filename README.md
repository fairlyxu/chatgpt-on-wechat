# 打包说明
-F表示单文件
-w表示没有docs框

## 1.先打包小助手

pyinstaller -F -i "desktop_app/desktop_vue_html/public/favicon.ico" --clean --add-data "config-template.json;."  --add-data "plugins/;plugins/" --name assistant assistan_start.py

## 2. 将小助手的打包assistant.exe复制到项目根目录下

## 3. 再打包客户端

pyinstaller -i "desktop_app/desktop_vue_html/public/favicon.ico" --clean --add-data "config-template.json;."  --add-data "assistant.exe;." --add-data "desktop_app/desktop_vue_html/dist;desktop_app/desktop_vue_html/dist" app.py

