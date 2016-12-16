# This IA:
# - abide the movement rules
# - choose a random next position

import random
from ia_utils import adjacent_moves, get_blocked_coords

def compute_ghost_pos(pos, level, _):
    moves = adjacent_moves(pos)
    for blocked_pos in get_blocked_coords(list(moves), level):
        moves.remove(blocked_pos)
    if not moves:
        return pos
    return random.choice(moves)
