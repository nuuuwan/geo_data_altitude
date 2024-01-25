import time


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.lap_time = self.start_time

    # def delta(self) -> float:
    #     return time.time() - self.start_time

    def lap(self) -> float:
        current_time = time.time()
        lap = current_time - self.lap_time
        self.lap_time = current_time
        return lap
