# encoding:utf-8

import argparse

import appDesktopMain
asistant_running = True  # 控制 run 函数的执行

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', type=str, help='配置文件目录', default="config.json")


if __name__ == "__main__":
    appDesktopMain.main()
