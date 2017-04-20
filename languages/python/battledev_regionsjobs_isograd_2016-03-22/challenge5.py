def debug(*args):
    try:
        local_print(' '.join(map(str, args)))
    except NameError:
        import sys; print(*args, file=sys.stderr)

from collections import defaultdict

N = int(input())
debug(N)

heights = []
pos_by_heights = defaultdict(list)
for i in range(N):
    height = int(input())
    heights.append(height)
    pos_by_heights[height].append(i)

length = 0
for height, indices in pos_by_heights.items():
    while len(indices) > 1:
        i = indices.pop(0)
        j = None
        obstacle_pos = i + 1
        while obstacle_pos < N and heights[obstacle_pos] <= height:
            obstacle_pos += 1
        while indices[0] <= obstacle_pos:
            j = indices.pop(0)
        if j is not None:
            length += j - i

print(length)
