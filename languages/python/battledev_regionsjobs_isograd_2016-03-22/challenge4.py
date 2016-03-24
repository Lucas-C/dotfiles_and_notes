N = int(input())
heights = []
for _ in range(N):
    height = int(input())
    heights.append(height)

for i in range(N):
    count = 0
    max_height = None
    # 1st pass: ahead
    for j in range(i + 1, N):
        if max_height is None or heights[j] > max_height:
            max_height = heights[j]
            count += 1
    # 1st pass: behind
    max_height = None
    for j in range(i - 1, -1, -1):
        if max_height is None or heights[j] > max_height:
            max_height = heights[j]
            count += 1
    if i != 0:
        print(' ', end='')
    print(count, end='')
