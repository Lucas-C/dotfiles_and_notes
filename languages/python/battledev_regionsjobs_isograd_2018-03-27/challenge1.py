from math import ceil
N = int(input())
best = None
for _ in range(N):
    x, y, z = list(map(int, input().split()))
    score = (x + y + z) / 3
    if not best or best < score:
        best = score
print(ceil(best))