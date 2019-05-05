#!/usr/bin/python

# For a given secret word, this program provides a sudoku-like (*) grid of letter,
# that when resolved reveals the hidden word on its diagonal starting from the top-left.

# (* : sudoku-like because letters replace digits and there is no concept of "boxes")

# Example: the word ENSEMBLE can produce this grid

#   E . . E . S . M
#   S . . B . E . .
#   . . S N E . B .
#   . M E . . L . .
#   L . N E . E . .
#   . L . . . . . E
#   N E . . E . . .
#   B . . L . . . E

import sys
from copy import deepcopy
from itertools import count, product
from random import choice, shuffle
from string import ascii_uppercase

try:
    from colorama import Fore, init  # optionnal dependency
    init()  # required for Windows
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = ColorFallback()

# Je fais une croix sur l'usage de numba pour le moment:
# - bug https://github.com/numba/numba/issues/4053
# - pas de support de np.argwhere
# - pas de support de np.setdiff1d / np.isin / np.in1d
# import numpy as np
# from numba import jit
# @jit(nopython=True)


if len(sys.argv) <= 1:
    raise RuntimeError('Please provide a word as argument to the program')
HIDDEN_WORD = sys.argv[1].upper()
GRID_SIZE = len(HIDDEN_WORD)
FILLING_RATIO = .6  # a good comprimise between hollow-enough grid and computing-time (given the current dummy generation algorithm)

LETTERS = set(HIDDEN_WORD)
while len(LETTERS) != GRID_SIZE:
    LETTERS.add(choice(ascii_uppercase))
LETTERS = list(HIDDEN_WORD)


def init_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        grid[i][i] = 1 + LETTERS.index(HIDDEN_WORD[i])
    return grid

def print_grid(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell = LETTERS[cell - 1] if cell else '.'
            if i == j:
                cell = Fore.RED + cell + Fore.RESET
            print(cell, end='')
        print()
    print()

def gen_puzzle_grid(grid):
    full_grid = next(solve_sudoku_nobox(init_grid()))
    # "Dummy" approach: we randomly puncture holes in the grid and hope it is has a unique solution.
    # This could be improved algorithmically and/or using numpy/numba, but so far it suffices to my needs.
    for _ in count(1):
        sys.stdout.write('.'); sys.stdout.flush()
        hollow_grid = deepcopy(full_grid)
        cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
        shuffle(cells)
        for i, j in cells[:int(FILLING_RATIO * GRID_SIZE * GRID_SIZE)]:
            hollow_grid[i][j] = 0
        if len(list(solve_sudoku_nobox(deepcopy(hollow_grid)))) == 1:
            return hollow_grid


### Code slightly adapted from: https://www.cs.mcgill.ca/~aassaf9/python/sudoku.txt
### Associated article: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

def solve_sudoku_nobox(grid):
    """ An efficient Sudoku solver using Algorithm X."""
    N = len(grid)
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

### END of Ali Assaf's code


if __name__ == '__main__':
    grid = gen_puzzle_grid()
    print(); print()
    print('Grid:')
    print_grid(grid)
    grid = next(solve_sudoku_nobox(grid))
    print('Solution:')
    print_grid(grid)
