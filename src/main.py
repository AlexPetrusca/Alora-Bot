import logging

from src.bot import Bot

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

Bot(play_count=5, debug=False).start()
