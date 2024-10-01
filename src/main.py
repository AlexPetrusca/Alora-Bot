import logging
from subprocess import Popen, DEVNULL
from src.bot import Bot

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

if __name__ == '__main__':
    keylogger = Popen(['python', './keylogger/keylog.py'], stdout=DEVNULL, stderr=DEVNULL)
    try:
        Bot(play_count=-1, debug=False).start()
    finally:
        keylogger.kill()
