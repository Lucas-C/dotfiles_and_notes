from hero_utils import allowed_moves_for, out_of_bounds


BLOCKED_TILES = ('#', 'X')


def get_allowed_moves(pos, level):
    return list(allowed_moves_for(pos, level, BLOCKED_TILES).values())

def iter_coords(pos, move, level):
    X, Y = len(level[0]), len(level)
    x, y = move
    dir_x, dir_y = x - pos[0], y - pos[1]
    while not out_of_bounds(x, y, X, Y) and level[y][x] not in BLOCKED_TILES:
        yield x, y
        x += dir_x
        y += dir_y
