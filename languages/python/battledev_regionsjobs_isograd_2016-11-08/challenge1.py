N = int(input())
from collections import defaultdict
gloves_counts = defaultdict(int)
for _ in range(N):
    color = input()
    gloves_counts[color] += 1
print(sum(c//2 for c in gloves_counts.values()))
