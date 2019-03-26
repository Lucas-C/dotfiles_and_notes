#!/usr/bin/python3
import sys
def local_print(*args): print(*args, file=sys.stderr)
pos = int(input())
local_print(pos)
for _ in range(42):
    runnes_before, runnes_after = list(map(int, input().split()))
    pos += runnes_before
    pos -= runnes_after
local_print(pos)
if 0 <= pos <= 100:
    print(1000)
elif pos > 10000:
    print('KO')
else:
    print(100)