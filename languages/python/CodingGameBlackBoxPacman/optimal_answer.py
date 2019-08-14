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


class Answer():
    def __init__(self, X, Y, Z):
        self.Y = int(X)
        self.X = int(Y)
        self.Z = int(Z)
        print('INIT:', self.X, self.Y, self.Z, file=sys.stderr)
        self.level = ['.'*self.X]*self.Y
        self.last_pos = None
        self.visits_count = defaultdict(int)
    def iteration(self, *args):
        neighbours = args[:4]
        coords = []
        for i in range(self.Z):
            coords.append([int(i) for i in args[i + 4].split()])
        ghosts_pos, pacman_pos = coords[:-1], tuple(coords[-1])
        update_level(self.level, pacman_pos, neighbours, ghosts_pos)
        render(self.level)
        dir, new_pos = choose_dir(self.level, pacman_pos, ghosts_pos, self.visits_count, self.last_pos)
        self.last_pos = pacman_pos
        self.visits_count[self.last_pos] += 1
        set_tile(self.level, pacman_pos, '_')
        return dir

def update_level(level, pacman_pos, neighbours, new_ghosts_pos):
    for pos in get_ghosts_pos(level):
        set_tile(level, pos, '_')
    for pos in new_ghosts_pos:
        set_tile(level, pos, 'X')
    set_tile(level, pacman_pos, 'H')
    x, y = pacman_pos
    set_tile(level, (x, y - 1), neighbours[0])  # block above
    set_tile(level, (x + 1, y), neighbours[1])  # block on the right
    set_tile(level, (x, y + 1), neighbours[2])  # block below
    set_tile(level, (x - 1, y), neighbours[3])  # block on the left

def set_tile(level, pos, char):
    x, y = pos
    level[y] = level[y][:x] + char + level[y][x+1:]

def get_ghosts_pos(level):
    for y, line in enumerate(level):
        for x in range(len(line)):
            if line[x] == 'X':
                yield x, y

def choose_dir(level, pos, ghosts, visited, last_pos):
    moves = allowed_moves_for(pos, level)
    # `moves` cannot be empty at this point (or else pacman started between 4 walls)
    if len(moves) == 1:  # dead-end
        return list(moves.items())[0]

    # 1- if there is a ghost closeby, run away !
    if ghosts_are_close_enough_to_worry(pos, ghosts):
        return safest_move(pos, moves, ghosts, level)

    # 2- if there is an unvisited tile around, go there !
    tiles_never_visited = {dir: move for dir, move in moves.items() if move not in visited}
    if tiles_never_visited:
        return sorted(tiles_never_visited.items())[0]

    # 3- else, go in the direction where there is the most unexplored tiles
    dir = unexplored_dir(pos, moves, level, last_pos)
    return dir, moves[dir]
