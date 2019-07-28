import sys

def render(level):
    X, Y = len(level[0]), len(level)
    for y in range(Y):
        for x in range(X):
            print(level[y][x], end='', file=sys.stderr)
        print('', file=sys.stderr)

def allowed_moves_for(pos, level, blocked_tiles=('#',)):
    x, y = pos
    moves = {
        'C': (x, y - 1), # up
        'A': (x + 1, y), # right
        'D': (x, y + 1), # down
        'E': (x - 1, y), # left
    }
    for dir in get_blocked_dirs(list(moves.items()), level, blocked_tiles):
        del moves[dir]
    return moves

def get_blocked_dirs(dir_pos_pairs, level, blocked_tiles):
    X, Y = len(level[0]), len(level)
    for dir, pos in dir_pos_pairs:
        x, y = pos
        if out_of_bounds(x, y, X, Y) or level[y][x] in blocked_tiles:
            yield dir

def out_of_bounds(x, y, X, Y):
    return x < 0 or x >= X or y < 0 or y >= Y
