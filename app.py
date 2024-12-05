# encoding:utf-8

import os
import signal
import sys

from channel import channel_factory
from common.log import logger
from config import conf, load_config
from plugins import *
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--config_file', type=str, help='配置文件目录', default="config.json")


def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def run(configfile=""):
    try:
        # load config
        load_config(configfile)
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"
            # os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:9001'

        channel = channel_factory.create_channel(channel_name)
        if channel_name in ["wx", "wxy", "terminal", "wechatmp", "wechatmp_service", "wechatcom_app", "wework"]:
            PluginManager().load_plugins()

        # startup channel
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)


if __name__ == "__main__":
    parser.parse_args()
    args = parser.parse_args()
    # 打印定位参数echo
    print(args.config_file)
    run(args.config_file)
