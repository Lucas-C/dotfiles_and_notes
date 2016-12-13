#!/usr/bin/python3

# IA ideas:
# - is ghost on same line / row ? If so:
#   * is there a block between them ?
#   * is in FRONT of Pacman ?
#   * is there a known path between them ?
# - compute dist to each ghost to detect dangerous ones
#   * if a ghost is closer than min(X,Y)/4 => go toward the largest adjacent area of the map where there's nobody

import sys
from collections import defaultdict

from gis import GHOSTINSIGHT_RISKFACTOR, get_riskiest_gis, get_aligned_pos_dir, select_escape_dir

Y = int(input())
X = int(input())
Z = int(input())
print('INIT:', X, Y, Z, file=sys.stderr)

level = ['.'*X]*Y
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

def render():
    for y in range(Y):
        for x in range(X):
            print(level[y][x], end='', file=sys.stderr)
        print('', file=sys.stderr)

def choose_dir(pos, ghosts):
    x, y = pos
    moves = {
        'C': (x, y - 1), # up
        'A': (x + 1, y), # right
        'D': (x, y + 1), # down
        'E': (x - 1, y), # left
    }

    # 1- We remove blocked tiles from the choices
    for dir in get_blocked_dirs(list(moves.items())):
        del moves[dir]
    # `moves` cannot be empty at this point (or else pacman started between 4 walls)

    # 2- If there is a ghost in sight, run away from him (gis = "ghost in sight")
    if len(moves) > 1:  # = not a dead-end
        gis_risk, gis_ghost = get_riskiest_gis(pos, ghosts, level)
        if gis_risk > GHOSTINSIGHT_RISKFACTOR:
            gis_dir = get_aligned_pos_dir(pos, gis_ghost)
            print('GhostInSight! risk=', gis_risk, 'dir=', gis_dir, file=sys.stderr)
            escape_dir = select_escape_dir(moves, gis_dir)
            print('Escaping GhostInSight: dir=', escape_dir, file=sys.stderr)
            return escape_dir, moves[escape_dir]

    def sort_key(item):
        dir, pos = item
        return (visits_count[pos], dir)
    return sorted(moves.items(), key=sort_key)[0]

def get_blocked_dirs(dir_pos_pairs):
    for dir, pos in dir_pos_pairs:
        x, y = pos
        if x == 0 or x == X or y == 0 or y == Y or level[y][x] == '#':
            yield dir

while True:
    neighbours = [input(), input(), input(), input()]
    coords = []
    for _ in range(Z):
        coords.append([int(i) for i in input().split()])
    ghosts_pos, pacman_pos = coords[:-1], tuple(coords[-1])
    update_level(pacman_pos, neighbours, ghosts_pos)
    render()
    dir, new_pos = choose_dir(pacman_pos, ghosts_pos)
    print(dir)
    last_visited = pacman_pos
    visits_count[last_visited] += 1
    set_tile(pacman_pos, '_')

