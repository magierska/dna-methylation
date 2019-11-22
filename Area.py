import math


class Area:
    count = 0

    def __init__(self, start, end, name=""):
        if start > end:
            raise ValueError
        self.start = start
        self.end = end
        self.name = name

    def __len__(self):
        return self.end - self.start + 1

    def middle(self):
        return self.start + math.ceil((self.end - self.start) / 2)

    def contains(self, value):
        if self.start <= value <= self.start + 1 or self.end - 1 <= value <= self.end:
            Area.count += 1
            print('%s %d %d %d \n' % (self.name, self.start, self.end, Area.count))
        return self.start <= value <= self.end

