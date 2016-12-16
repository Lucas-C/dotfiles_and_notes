#!/usr/bin/python3

import importlib, sys, time

def read_level(level_filename):
    with open(level_filename) as level_file:
        return [line.strip() for line in level_file.readlines()]

def dbg_display_level(level):
    print('\n'.join(level), file=sys.stderr)

def print_cg_init(level):
    print(len(level))
    print(len(level[0]))
    print(1 + sum(line.count('X') for line in level))

def print_cg_formatted_level(level, ghosts):
    pacman_pos = get_pacman_pos(level)
    for neighbour_block in get_pacman_neighbour_blocks(level, pacman_pos):
        print(neighbour_block, file=sys.stderr)
        print(neighbour_block)
    for ghost_pos in ghosts:
        print(*ghost_pos, file=sys.stderr)
        print(*ghost_pos)
    print(*pacman_pos, file=sys.stderr)
    print(*pacman_pos)

def get_pacman_neighbour_blocks(level, pacman_pos):
    x, y = pacman_pos
    neighbour_blocks = level[y - 1][x], level[y][x + 1], level[y + 1][x], level[y][x - 1]
    return [block if block != 'X' else '#' for block in neighbour_blocks]  # TODO: TEST IF CONFORM TO CODINGGAME

def get_pacman_pos(level):
    for y, line in enumerate(level):
        if 'H' in line:
            return line.index('H'), y

def get_ghosts_pos(level):
    for y, line in enumerate(level):
        for x in range(len(line)):
            if line[x] == 'X':
                yield x, y

def move_pacman(level, dir):
    moves = {
        'A': lambda x, y: (x + 1, y),
        'B': lambda x, y: (x, y),
        'C': lambda x, y: (x, y - 1),
        'D': lambda x, y: (x, y + 1),
        'E': lambda x, y: (x - 1, y),
    }
    old_pacman_pos = get_pacman_pos(level)
    set_tile(level, old_pacman_pos, '_')
    new_pacman_pos = moves[dir](*old_pacman_pos)
    set_tile(level, new_pacman_pos, 'H')

def set_tile(level, pos, char):
    x, y = pos
    level[y] = level[y][:x] + char + level[y][x+1:]

def check_pacman_eaten(ghost_pos, level):
    x, y = ghost_pos
    if level[y][x] == 'H':
        raise PacmanEaten

class PacmanEaten(Exception): pass

level = read_level(sys.argv[1])
ghosts = list(get_ghosts_pos(level))
ghosts_memory = [{} for _ in ghosts]
ia = importlib.import_module(sys.argv[2].split('.')[0])
dbg_display_level(level)
print_cg_init(level)
while True:
    print_cg_formatted_level(level, ghosts)
    time.sleep(.1)
    pacman_dir = input()
    print(pacman_dir, file=sys.stderr)
    move_pacman(level, pacman_dir)
    for i, old_ghost_pos in enumerate(ghosts):
        set_tile(level, old_ghost_pos, '_')
        print('Ghost #', i, file=sys.stderr)
        ghosts[i] = ia.compute_ghost_pos(old_ghost_pos, level, ghosts_memory[i])
        check_pacman_eaten(ghosts[i], level)
        set_tile(level, ghosts[i], 'X')
