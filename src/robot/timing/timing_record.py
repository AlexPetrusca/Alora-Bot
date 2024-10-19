class TimingRecord:
    def __init__(self, tick, status, prev_status=None, play_count=0):
        self.tick = tick
        self.status = status
        self.prev_status = prev_status  # observer() only
        self.play_count = play_count  # interval(), poll() only
