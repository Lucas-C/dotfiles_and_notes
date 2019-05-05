#!/usr/bin/python

# cf. https://chezsoi.org/lucas/blog/hiding-secret-words-in-sudokus-with-python.html

# For a given secret word, this program provides a sudoku grid of letter,
# that when resolved reveals the hidden word on its diagonal starting from the top-left.

# Examples:

# ./secret_word_sudokulike_grid_generator.py ensemble
#   ..L.|...J               EMLS|BNKJ
#   BNK.|...L               BNKJ|EMSL
#   ---------               ---------
#   ....|....               MLSB|JENK
#   J..E|.S.M               JKNE|LSBM
#   ---------   solution:   ---------
#   S..K|....               SBJK|MLEN
#   L..N|KB.S               LEMN|KBJS
#   ---------               ---------
#   .J.M|.KLB               NJEM|SKLB
#   .S.L|..ME               KSBL|NJME

# ./secret_word_sudokulike_grid_generator.py --no-boxes-constraint ensemble
#   E . M . . L . .               E D M S N L Q B
#   . N . M . . S L               Q N D M B E S L
#   B E . . . . . N               B E S L Q D M N
#   . . . . . . . .   solution:   N S B E L Q D M
#   D . L B . N . S               D Q L B M N E S
#   . M E . . . N .               L M E D S B N Q
#   S B . . E . . D               S B Q N E M L D
#   . . . Q D S B .               M L N Q D S B E

import argparse, math, sys
from copy import deepcopy
from functools import reduce
from itertools import product
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


FILLING_RATIO = .6  # a good comprimise between hollow-enough grid and computing-time (given the current dummy generation algorithm)


def main():
    args = parse_args()
    if args.boxes_dims:
        print('Boxes dimensions:', args.boxes_dims)
    else:
        print('Pseudo-sudoku : puzzle will have no boxes constraint')
    grid = gen_puzzle_grid(args)
    print()
    print('Grid:')
    print_grid(grid, args)
    grid = next(solve_sudoku(grid, args.boxes_dims))
    print('Solution:')
    print_grid(grid, args)

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('hidden_word', help=' ')
    parser.add_argument('--no-boxes-constraint', action='store_true', help=' ')
    parser.add_argument('--require-each-letter-in-grid', action='store_true', help=' ')
    args = parser.parse_args()
    args.hidden_word = args.hidden_word.upper()
    setattr(args, 'grid_size', len(args.hidden_word))
    letters = set(args.hidden_word)
    while len(letters) != args.grid_size:
        letters.add(choice(ascii_uppercase))
    setattr(args, 'letters', list(letters))
    setattr(args, 'boxes_dims', None if args.no_boxes_constraint else biggest_factors(args.grid_size))
    return args

def biggest_factors(n):
    'Returns None if prime'
    factors = set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if not n % i)))
    if len(factors) == 2:
        return None
    for i in range(int(math.sqrt(n)), 0, -1):
        if i in factors:
            return (i, n // i)

def print_grid(grid, args):
    for i, row in enumerate(grid):
        if args.boxes_dims and i > 0 and not i % args.boxes_dims[0]:
            print('-' * (len(grid) + args.boxes_dims[0] - 1))
        for j, cell in enumerate(row):
            cell = args.letters[cell - 1] if cell else '.'
            if i == j:
                cell = Fore.RED + cell + Fore.RESET
            if j > 0:
                if args.boxes_dims:
                    if not j % args.boxes_dims[1]:
                        print('|', end='')
                else:
                    print(' ', end='')
            print(cell, end='')
        print()
    print()

def gen_puzzle_grid(args):
    full_grid = next(solve_sudoku(init_grid(args), args.boxes_dims))
    # "Dummy" approach: we randomly puncture holes in the grid and hope it is has a unique solution.
    # This could be improved algorithmically and/or using numpy/numba, but so far it suffices to my needs.
    while True:
        sys.stdout.write('.'); sys.stdout.flush()
        hollow_grid = deepcopy(full_grid)
        cells = [(i, j) for i in range(args.grid_size) for j in range(args.grid_size)]
        shuffle(cells)
        for i, j in cells[:int(FILLING_RATIO * args.grid_size ** 2)]:
            hollow_grid[i][j] = 0
        if args.require_each_letter_in_grid:
            count_uses = lambda grid, letter: sum(row.count(letter) for row in grid)
            if any(count_uses(hollow_grid, l) == 0 for l in args.letters):
                continue
        if len(list(solve_sudoku(deepcopy(hollow_grid), args.boxes_dims))) == 1:
            return hollow_grid

def init_grid(args):
    'Creates an empty grid with just the hidden word on the diagonal'
    grid = [[0] * args.grid_size for _ in range(args.grid_size)]
    for i in range(args.grid_size):
        grid[i][i] = 1 + args.letters.index(args.hidden_word[i])
    return grid


### Code from: https://www.cs.mcgill.ca/~aassaf9/python/sudoku.txt
### Associated article: https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

# Author: Ali Assaf <ali.assaf.mail@gmail.com>
# Copyright: (C) 2010 Ali Assaf
# License: GNU General Public License <http://www.gnu.org/licenses/>

def solve_sudoku(grid, boxes_dims=None):
    """
    An efficient Sudoku solver using Algorithm X.
    The box constraint is only added if boxes_dims is provided.
    """
    N = len(grid)
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))])
    if boxes_dims:
        X += [("bn", bn) for bn in product(range(N), range(1, N + 1))]
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n))]
        if boxes_dims:
            R, C = boxes_dims
            b = (r // R) * R + (c // C) # Box number
            Y[(r, c, n)].append(("bn", (b, n)))
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
    main()
