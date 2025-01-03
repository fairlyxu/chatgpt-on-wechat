# encoding:utf-8

import signal
import sys
import argparse
from channel import channel_factory
from config import load_config
from plugins import *

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', type=str, help='配置文件目录', default="config-template.json")


def handle_sigterm(signum, frame):
    conf().save_user_datas()
    print("Received SIGTERM signal. Shutting down gracefully...")
    sys.exit(0)

def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)
    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def run(configfile=""):
    try:
        # load config
        load_config(configfile)
        # 注册SIGTERM处理器，以便优雅地关闭
        #signal.signal(signal.SIGTERM, handle_sigterm)
        # ctrl + c
        #sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        #sigterm_handler_wrap(signal.SIGTERM)

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
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)



if __name__ == "__main__":
    print("asistant is starting...")
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "config-template.json"

    run(config_file)
