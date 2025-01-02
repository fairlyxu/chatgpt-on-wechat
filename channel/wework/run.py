import os
import time
import traceback

os.environ['ntwork_LOG'] = "ERROR"
import ntwork

wework = ntwork.WeWork()


def forever():
    try:
        while True:
            time.sleep(0.1)
    except Exception as e:
        traceback.print_exc()
        print("EXCEPTION FOUND: " + str(e))
        #os._exit(0)


