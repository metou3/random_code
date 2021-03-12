import os
import sys
import time
import datetime

if __name__ == "__main__":
    flask_app = sys.argv[1]
    while True:
        stream = os.popen("ps -ax | grep python3")
        if os.path.join(os.getcwd(), flask_app) not in stream.read():
            print(datetime.datetime.utcnow(), " restarting... " + flask_app)
            os.system("sudo nohup python3 "+flask_app+" &")
        else:
            time.sleep(60)
            pass

