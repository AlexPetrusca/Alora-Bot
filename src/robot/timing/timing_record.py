class TimingRecord:
    def __init__(self, tick, status, prev_status=None):
        self.tick = tick
        self.status = status
        self.prev_status = prev_status
