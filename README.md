# 打包说明
pyinstaller -F -w -i "desktop_app/desktop_vue_html/public/favicon.ico" --clean --add-data "config-template.json:."  --add-data "desktop_app/desktop_vue_html/dist;desktop_app/desktop_vue_html/dist" app.py

pyinstaller -F -w -i "desktop_app/desktop_vue_html/public/favicon.ico" --clean --add-data "config-template.json:."  --name assistant assistan_start.py