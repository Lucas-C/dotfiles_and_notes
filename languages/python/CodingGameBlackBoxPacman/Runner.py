#!/usr/bin/python3

# A CLI "process" runner, reading on stdin & writing on stdout

import importlib, sys, time


def main(level, ia_name_or_path, sleep, write_output, get_pacman_dir):
    ghosts = list(get_ghosts_pos(level))
    ghosts_memory = [{} for _ in ghosts]
    ia = importlib.import_module(ia_name_or_path.split('.')[0])
    dbg_display_level(level)
    print_cg_init(write_output, level)
    while True:
        print_cg_formatted_level(write_output, level, ghosts)
        if sleep:
            time.sleep(sleep)
        pacman_dir = get_pacman_dir()
        debug_print(pacman_dir)
        move_pacman(level, pacman_dir)
        for i, old_ghost_pos in enumerate(ghosts):
            set_tile(level, old_ghost_pos, '_')
            ghosts[i] = ia.compute_ghost_pos(old_ghost_pos, level, ghosts_memory[i])
            check_pacman_eaten(ghosts[i], level)
            set_tile(level, ghosts[i], 'X')

def read_level(level_filename):
    with open(level_filename) as level_file:
        return [line.strip() for line in level_file.readlines()]

def dbg_display_level(level):
    debug_print('\n'.join(level))

def print_cg_init(write_output, level):
    write_output(len(level))
    write_output(len(level[0]))
    write_output(1 + sum(line.count('X') for line in level))

def print_cg_formatted_level(write_output, level, ghosts):
    pacman_pos = get_pacman_pos(level)
    for neighbour_block in get_pacman_neighbour_blocks(level, pacman_pos):
        debug_print(neighbour_block)
        write_output(neighbour_block)
    for ghost_pos in ghosts:
        debug_print(*ghost_pos)
        write_output(*ghost_pos)
    debug_print(*pacman_pos)
    write_output(*pacman_pos)

def get_pacman_neighbour_blocks(level, pacman_pos):
    x, y = pacman_pos
    neighbour_blocks = level[y - 1][x], level[y][x + 1], level[y + 1][x], level[y][x - 1]
    return [block for block in neighbour_blocks]  # TODO: TEST IF CONFORM TO CODINGGAME

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
    if dir not in moves:
        raise ValueError('Invalid value provided')
    new_pacman_pos = moves[dir](*old_pacman_pos)
    x, y = new_pacman_pos
    if level[y][x] not in ('_', 'H'):
        raise ValueError('Cannot move there')
    set_tile(level, old_pacman_pos, '_')
    set_tile(level, new_pacman_pos, 'H')

def set_tile(level, pos, char):
    x, y = pos
    level[y] = level[y][:x] + char + level[y][x+1:]

def check_pacman_eaten(ghost_pos, level):
    x, y = ghost_pos
    if level[y][x] == 'H':
        raise GameOver('They got you')

class GameOver(Exception): pass

DEBUG = True

def debug_print(*args):
    if DEBUG:
        print(*args, file=sys.stderr)


if __name__ == '__main__':
    main(read_level(sys.argv[1]), sys.argv[2], .1, print, input)
