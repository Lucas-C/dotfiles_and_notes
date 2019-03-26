#!/usr/bin/python3
# USAGE: echo 'Xo**o*' | python -c 's=input(); print(len(s)); print(s)' | ./challenge5.py
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
level = input()
local_print(level)
def pos_with_char(char):
    for i, l in enumerate(level):
        if l == char:
            yield i
initial_pos = next(pos_with_char('X'))
explored_range = [initial_pos, initial_pos]
output = ''
while explored_range != [0, N-1]:
    # local_print(level)
    # local_print('explored_range:', explored_range)
    i, j = explored_range[0] - 1, explored_range[1] + 1
    i2, j2 = i, j
    while i2 >= 0 and j2 < N and level[i2] == level[j2]:
        i2 -= 1
        j2 += 1
    # local_print('i2/j2:', i2, j2)
    if j2 >= N or (i2 >= 0 and level[i2] == 'o'):
        output += level[i]
        level = level[:i] + '.' + level[i+1:]
        explored_range[0] = i
    else:
        output += level[j]
        level = level[:j] + '.' + level[j+1:]
        explored_range[1] = j
print(output)
