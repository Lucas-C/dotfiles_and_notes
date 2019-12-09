#!/usr/bin/env python3

# For a given secret word of max 27 letters, this program provides a 3-colored sudoku grid,
# that when solved reveals the hidden word.

# TODO: improving display as currently "dimmed" empty green cells
#       are very hard to distinguish from grey (dimmed white) ones

# USAGE:
#   PYTHONPATH=. ./colored_sudoku_grid_generator.py 'te quiero'

# TESTS:
#   PYTHONPATH=. pytest colored_sudoku_grid_generator.py

# GLOSSARY:
#   puzzle_grid = colored_grid = sudoku_grid + color_grid

import argparse
from copy import deepcopy
from random import shuffle
from string import ascii_uppercase

from colorama import Fore, Style, init
init()  # required for Windows

from secret_word_sudokulike_grid_generator import gen_sudoku_grid, solve_sudoku

GRID_SIZE = 9
GRID_BOXES_DIMS = (3, 3)
COLORS = ('RED', 'GREEN', 'BLUE')


def main():
    args = parse_args()
    colored_grid, hidden_word_coords = gen_puzzle_grid(args)
    print('\n')
    print('Grid:')
    print_colored_grid(colored_grid, hidden_word_coords)
    print('Hidden word letters coords:', sorted(hidden_word_coords))
    print()
    print('Deciphering table:')
    print_cipher_table()
    print()
    print('Solution:')
    colored_grid = solve_colored_grid(colored_grid)
    print_colored_grid(colored_grid, hidden_word_coords)

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('hidden_word', help=' ')
    parser.add_argument('--max-colored-cells', type=int, default='33', help=' ')
    args = parser.parse_args()
    args.hidden_word = args.hidden_word.upper()
    return args

def gen_puzzle_grid(args):
    while True:
        hollow_colored_grid = init_colored_grid(args)
        hidden_word_coords = set((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if hollow_colored_grid[i][j][1])
        # print('Hollow grid attempt:')
        # print_colored_grid(hollow_colored_grid, hidden_word_coords)
        try:
            full_sudoku_grid = next(solve_sudoku(colored_grid2sudoku_grid(hollow_colored_grid), GRID_BOXES_DIMS))
            full_color_grid = next(fill_color_grid(colored_grid2color_grid(hollow_colored_grid)))
            hollow_color_grid = next(gen_color_grid(full_color_grid, args.max_colored_cells))
            break
        except StopIteration:
            pass
    # print('Full grid:')
    # print_colored_grid(add_colors(full_sudoku_grid, full_color_grid), hidden_word_coords)
    hollow_sudoku_grid = gen_sudoku_grid(full_sudoku_grid, GRID_BOXES_DIMS)
    return add_colors(hollow_sudoku_grid, hollow_color_grid), hidden_word_coords

def init_colored_grid(args):
    'Creates an empty grid with just the hidden word on the diagonal'
    grid = [[('', 0)] * GRID_SIZE for _ in range(GRID_SIZE)]
    if recur_init_grid(grid, args.hidden_word):
        return grid
    raise RuntimeError('Cannot generate a valid grid')

def recur_init_grid(grid, letters, k=0):
    if not letters:
        return True
    if k >= 27:
        return False
    color, digit = cell_for_letter(letters[0])
    i = k // 3
    increments = [0, 1, 2]
    shuffle(increments)
    for n in increments:
        j = 3*(k % 3) + n
        if any(grid[i2][j][1] == digit for i2 in range(GRID_SIZE)):
            continue
        if any(grid[i][j2][1] == digit for j2 in range(GRID_SIZE)):
            continue
        if any(grid[i2][j2][1] == digit for i2 in range(3*(i // 3), 3*(i // 3) + 3)
                                        for j2 in range(3*(j // 3), 3*(j // 3) + 3)):
            continue
        if any(cell[0] == color for cell in neighbours(grid, i, j)):
            continue
        grid[i][j] = (color, digit)
        if recur_init_grid(grid, letters[1:], k + 1):
            return True
        # Undo:
        grid[i][j] = ('', 0)
    return recur_init_grid(grid, letters, k + 1)

def neighbours(grid, i, j):
    grid_size = len(grid)
    if i - 1 >= 0:
        yield grid[i-1][j]
    if i + 1 < grid_size:
        yield grid[i+1][j]
    if j - 1 >= 0:
        yield grid[i][j-1]
    if j + 1 < grid_size:
        yield grid[i][j+1]

def fill_color_grid(hollow_color_grid):
    grid_size = len(hollow_color_grid)
    colored_grid =  [[hollow_color_grid[i][j] for j in range(grid_size)]
                                              for i in range(grid_size)]
    yield from recur_fill_grid(colored_grid)

def recur_fill_grid(colored_grid, i=0, j=0):
    grid_size = len(colored_grid)
    if j == grid_size:
        yield colored_grid
        return
    next_i, next_j = i + 1, j
    if next_i == grid_size:
        next_i, next_j = 0, j + 1
    if colored_grid[i][j]:
        # Already initially filled
        yield from recur_fill_grid(colored_grid, next_i, next_j)
    else:
        colors = list(COLORS)
        shuffle(colors)
        for color in colors:
            if any(cell == color for cell in neighbours(colored_grid, i, j)):
                continue
            colored_grid[i][j] = color
            yield from recur_fill_grid(colored_grid, next_i, next_j)

def gen_color_grid(full_color_grid, max_colored_cells):
    # Same "dummy" approach as gen_sudoku_grid: we randomly puncture holes in the grid and hope it is has a unique solution.
    grid_size = len(full_color_grid)
    color_grid = [[full_color_grid[i][j] for j in range(grid_size)]
                                         for i in range(grid_size)]
    print('Generatig color grid with holes:')
    while True:
        print('.', end='', flush=True)
        color_grid = recur_gen_color_grid(color_grid)
        if not max_colored_cells or sum(1 for j in range(grid_size) for i in range(grid_size) if color_grid[i][j]) <= max_colored_cells:
            print()
            yield color_grid

def test_recur_gen_color_grid():
    grid = [['RED',  'GREEN', 'BLUE' ],
            ['BLUE', 'RED',   'GREEN'],
            ['RED',  'GREEN', 'BLUE' ]]
    grid = recur_gen_color_grid(grid)
    assert grid
    grid_size = len(grid)
    colored_cells_count = sum(1 for j in range(grid_size) for i in range(grid_size) if grid[i][j])
    assert colored_cells_count <= 4

def recur_gen_color_grid(color_grid):
    grid_size = len(color_grid)
    coords = [(i, j) for j in range(grid_size) for i in range(grid_size) if color_grid[i][j]]
    shuffle(coords)
    for (i, j) in coords:
        color = color_grid[i][j]
        color_grid[i][j] = ''
        if solve_color_grid(color_grid):
            return recur_gen_color_grid(color_grid)
        color_grid[i][j] = color  # revert change
    return color_grid

def test_solve_color_grid():
    grid = [['RED',  '',      'BLUE'],
            ['BLUE', 'RED',   ''    ],
            ['',     '',      'BLUE']]
    assert solve_color_grid(grid)

def solve_color_grid(color_grid):
    grid_size = len(color_grid)
    grid = [[color_grid[i][j] for j in range(grid_size)]
                              for i in range(grid_size)]
    while any(not grid[i][j] for j in range(grid_size) for i in range(grid_size)):
        color_added = False
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j]:
                    continue
                near_colors = set(neighbours(grid, i, j)) - {''}
                if len(near_colors) == 3:
                    return None
                elif len(near_colors) == 2:
                    missing_color = list(set(COLORS) - near_colors)[0]
                    grid[i][j] = missing_color
                    color_added = True
        if not color_added:
            return None
    return grid

def solve_colored_grid(colored_grid):
    sudoku_grid = colored_grid2sudoku_grid(colored_grid)
    color_grid = colored_grid2color_grid(colored_grid)
    return add_colors(next(solve_sudoku(sudoku_grid, GRID_BOXES_DIMS)), solve_color_grid(color_grid))

def print_colored_grid(colored_grid, bold_coords=()):
    for i, row in enumerate(colored_grid):
        if i > 0 and not i % 3:
            print('-' * (len(colored_grid) + 2))
        for j, cell in enumerate(row):
            val = str(cell[1] or '.')
            color = cell[0] or 'WHITE'
            char = getattr(Fore, color) + val + Fore.RESET
            if (i, j) in bold_coords:
                char = Style.DIM + char + Style.RESET_ALL
            if j > 0:
                if not j % 3:
                    print('|', end='')
            print(char, end='')
        print()
    print()

def print_cipher_table():
    print(             '     |' + '|'.join(map(str, range(1, 10))))
    print(Fore.RED   + '  RED|' + '|'.join(ascii_uppercase[:9])         + Fore.RESET)
    print(Fore.GREEN + 'GREEN|' + '|'.join(ascii_uppercase[9:18])       + Fore.RESET)
    print(Fore.BLUE  + ' BLUE|' + '|'.join(ascii_uppercase[18:26] + ' ') + Fore.RESET)

def colored_grid2sudoku_grid(colored_grid):
    return [[colored_grid[i][j][1] for j in range(GRID_SIZE)]
                                   for i in range(GRID_SIZE)]

def colored_grid2color_grid(colored_grid):
    return [[colored_grid[i][j][0] for j in range(GRID_SIZE)]
                                   for i in range(GRID_SIZE)]

def add_colors(sudoku_grid, color_grid):
    return [[(color_grid[i][j], sudoku_grid[i][j]) for j in range(GRID_SIZE)]
                                                   for i in range(GRID_SIZE)]

def cell_for_letter(letter):
    val = 26 if letter == ' ' else ord(letter) -  ord('A')
    color = COLORS[val // 9]
    digit = 1 + (val % 9)
    return (color, digit)

if __name__ == '__main__':
    main()
