import time, datetime


class Chronometer:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def start(self):
        self.start_time = time.time()
        return self.start_time

    def stop(self):
        self.stop_time = time.time()
        return self.stop_time

    def get_elapsed_time(self):
        r = self.stop_time - self.start_time
        st3 = datetime.datetime.fromtimestamp(r).strftime('%M:%S')
        return st3
