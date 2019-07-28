# This IA:
# - abide the movement rules
# - choose a random next position

import random
from ia_utils import get_allowed_moves

def compute_ghost_pos(pos, level, _):
    moves = get_allowed_moves(pos, level)
    if not moves:
        return pos
    return random.choice(moves)
