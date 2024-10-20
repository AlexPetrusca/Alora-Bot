import traceback as tb


class Mutex:
    def __init__(self):
        self.owner = None

    def acquire(self, force=False):
        if force:
            self.owner = Mutex.get_request_identifier()
            return True

        identity = Mutex.get_request_identifier()
        if not self.locked():
            self.owner = Mutex.get_request_identifier()
            return True
        else:
            return self.owner == identity

    def release(self, force=False):
        if force:
            self.owner = None
            return True

        identity = Mutex.get_request_identifier()
        if identity == self.owner and self.locked():
            self.owner = None
            return True
        elif identity != self.owner:
            raise AssertionError("Cannot release a mutex that was not previously acquired: "
                                 f"owner id '{self.owner}' does not match '{identity}'")
        else:
            raise AssertionError("Cannot release an unlocked mutex")

    def locked(self):
        return self.owner is not None

    @classmethod
    def get_request_identifier(cls):
        stack = tb.extract_stack()
        for frame in reversed(stack):
            if not frame.filename.endswith("timing/timing.py") and not frame.filename.endswith("timing/mutex.py"):
                return f"{frame.filename}_{frame.name}"
        return None
