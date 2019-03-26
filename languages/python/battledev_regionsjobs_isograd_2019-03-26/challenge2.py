#!/usr/bin/python3
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
count = 1
weight = 0
for _ in range(N):
    P = int(input())
    weight += P
    if weight > 100:
        count += 1
        weight = P
print(count)
