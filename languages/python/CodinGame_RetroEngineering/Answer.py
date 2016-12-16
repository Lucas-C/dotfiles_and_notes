#!/usr/bin/python3
#--------------------------------------------------------------------------------------------------#

# IA ideas:
# - take into considerations known paths
# - per-dir ghost risk

from hero_utils import render, allowed_moves_for
from hero_ghostcloseby import ghosts_are_close_enough_to_worry, safest_move
from hero_explorerinstinct import unexplored_dir

import sys
from collections import defaultdict


Y = int(input())
X = int(input())
Z = int(input())
print('INIT:', X, Y, Z, file=sys.stderr)

level = ['.'*X]*Y
second2last_pos, last_pos = None, None
visits_count = defaultdict(int)

def update_level(pacman_pos, neighbours, new_ghosts_pos):
    for pos in get_ghosts_pos():
        set_tile(pos, '_')
    for pos in new_ghosts_pos:
        set_tile(pos, 'X')
    set_tile(pacman_pos, 'H')
    x, y = pacman_pos
    set_tile((x, y - 1), neighbours[0])  # block above
    set_tile((x + 1, y), neighbours[1])  # block on the right
    set_tile((x, y + 1), neighbours[2])  # block below
    set_tile((x - 1, y), neighbours[3])  # block on the left

def set_tile(pos, char):
    x, y = pos
    level[y] = level[y][:x] + char + level[y][x+1:]

def get_ghosts_pos():
    for y, line in enumerate(level):
        for x in range(len(line)):
            if line[x] == 'X':
                yield x, y

def choose_dir(pos, ghosts):
    moves = allowed_moves_for(pos, level)
    # `moves` cannot be empty at this point (or else pacman started between 4 walls)
    if len(moves) == 1:  # dead-end
        return list(moves.items())[0]

    # 1- if there is a ghost closeby, run away !
    if ghosts_are_close_enough_to_worry(pos, ghosts):
        return safest_move(pos, moves, ghosts, level)

    # 2- if there is an unvisited tile around, go there !
    tiles_never_visited = {dir: move for dir, move in moves.items() if move not in visits_count}
    if tiles_never_visited:
        return sorted(tiles_never_visited.items())[0]

    # 3- else, go in the direction where there is the most unexplored tiles
    return unexplored_dir(moves, level, last_pos)

while True:
    neighbours = [input(), input(), input(), input()]
    coords = []
    for _ in range(Z):
        coords.append([int(i) for i in input().split()])
    ghosts_pos, pacman_pos = coords[:-1], tuple(coords[-1])
    update_level(pacman_pos, neighbours, ghosts_pos)
    render(level)
    dir, new_pos = choose_dir(pacman_pos, ghosts_pos)
    print(dir)
    second2last_pos = last_pos
    last_pos = pacman_pos
    visits_count[last_pos] += 1
    set_tile(pacman_pos, '_')

