import json


class Watcher:
    def __init__(self):
        self.key_toggles = set()
        self.key_strokes = list()

    def watch(self, key_code):
        self.key_strokes.insert(0, key_code)
        while len(self.key_strokes) > 10:
            self.key_strokes.pop()

        if key_code in self.key_toggles:
            self.key_toggles.remove(key_code)
        else:
            self.key_toggles.add(key_code)

    def get_key_toggles_as_json(self):
        return json.dumps({"keys": list(self.key_toggles)})

    def get_key_strokes_as_json(self):
        return json.dumps({"keys": self.key_strokes})
