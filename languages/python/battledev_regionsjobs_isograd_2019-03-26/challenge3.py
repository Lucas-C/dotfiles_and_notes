#!/usr/bin/python3
# i=1; ./challenge3_compute_score.py $(./challenge3.py < chall3/input$i.txt) < chall3/input$i.txt; ./challenge3_compute_score.py $(cat chall3/output$i.txt) < chall3/input$i.txt
import sys
def local_print(*args): print(*args, file=sys.stderr)
N = int(input())
level = [input() for i in range(N)]
local_print('\n'.join(level))
dir = '>'
first_pass = []
for _ in range(N):
    if first_pass:
        first_pass += 'v'
    first_pass.extend(dir * (N - 1))
    dir = '<' if dir == '>' else '>'
# local_print(first_pass)
second_pass = []
for _ in range(N):
    if second_pass:
        second_pass += '^'
    second_pass.extend(dir * (N - 1))
    dir = '<' if dir == '>' else '>'
# local_print(second_pass)
i, j = 0, 0  # position: i = line/row, j = column
def list_moves(moves, target_char):
    global i, j
    for char in moves:
        if level[i][j] == target_char:
            yield 'x'
        if char == '<':
            j -= 1
        elif char == '>':
            j += 1
        elif char == '^':
            i -= 1
        elif char == 'v':
            i += 1
        yield char
    if level[i][j] == target_char:
        yield 'x'
output = ''.join(list_moves(first_pass, 'o')) + ''.join(list_moves(second_pass, '*'))
print(output)