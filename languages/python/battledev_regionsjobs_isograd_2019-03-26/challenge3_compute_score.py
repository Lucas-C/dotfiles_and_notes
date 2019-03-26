#!/usr/bin/python3
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
level = [input() for i in range(N)]
i, j = 0, 0  # position: i = line/row, j = column
score = 0
for char in sys.argv[1]:
    if char == '<':
        j -= 1
    elif char == '>':
        j += 1
    elif char == '^':
        i -= 1
    elif char == 'v':
        i += 1
    if char == 'x':
        if level[i][j] == 'o':
            score += 1
        if level[i][j] == '*':
            score *= 2
print(score)