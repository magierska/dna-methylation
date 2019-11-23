import math


class Area:
    def __init__(self, start, end, name=""):
        if start >= end:
            raise ValueError
        self.start = start
        self.end = end
        self.name = name

    def __len__(self):
        return self.end - self.start

    def middle(self):
        return self.start + math.ceil(len(self) / 2)

    def contains(self, value):
        return self.start <= value < self.end

