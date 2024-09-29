from requests import request

from src.actions.action import Action

TICK_INTERVAL = 0.1  # 100ms tick
KEYLOGGER_HOST = "http://localhost:8080"


class BackgroundScript:
    bot = None
    key_toggles = set()

    t_last = 0

    def __init__(self, bot):
        self.bot = bot

    def tick(self, t):
        if t - self.t_last > TICK_INTERVAL:
            res = request("GET", f"{KEYLOGGER_HOST}/keyStrokes")
            if res.ok:
                for key in res.json()['keys']:
                    if key in self.key_toggles:
                        self.untoggle_key(key)
                    else:
                        self.toggle_key(key)
            self.t_last = t

    def toggle_key(self, key):
        if type(key) is not int:
            key = key.value
        self.key_toggles.add(key)

    def untoggle_key(self, key):
        if type(key) is not int:
            key = key.value
        self.key_toggles.remove(key)

    def key_toggled(self, key):
        if type(key) is not int:
            key = key.value
        return key in self.key_toggles
        