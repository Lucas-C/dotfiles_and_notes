##
## Solution by ISOGRAD, customized by Lucas-C
##
N = int(input())
heights = []
pos = {}
for i in range(N):
    height = int(input())
    heights.append(height)
    pos.setdefault(height, []).append(i)

class RangeMaxQuery:
    GUARD = -1
    def __init__(self, positive_values):
        self.N = 1
        while self.N < len(positive_values):
            self.N *= 2
        self.s = [self.GUARD] * (2 * self.N)
        for i in range(len(positive_values)):
            self.s[self.N + i] = positive_values[i]
        for p in range(self.N - 1, 0, -1):
            self.s[p] = max(self.s[2 * p], self.s[2 * p + 1])

    def max_in_range(self, i, k):
        return self._range_max(1, 0, self.N, i, k)

    def _range_max(self, p, start, span, i, k):
        if start + span <= i or k <= start:
            return self.GUARD
        if i <= start and start + span <= k:
            return self.s[p]
        left  = self._range_max(2*p,     start,             span // 2, i, k)
        right = self._range_max(2*p + 1, start + span // 2, span // 2, i, k)
        return max(left, right)

length = 0
rmq = RangeMaxQuery(heights)
for height in pos:
    for i in range(1, len(pos[height])):
        start = pos[height][i - 1]
        end = pos[height][i]
        highest_between = rmq.max_in_range(start + 1, end)
        if highest_between < height:
            length += end - start
print(length)
