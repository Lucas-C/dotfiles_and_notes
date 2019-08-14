# This IA:
# - abide the movement rules
# - choose a random next position, that is NOT its previous one

import random
from ia_utils import get_allowed_moves

def compute_ghost_pos(pos, level, memory):
    moves = get_allowed_moves(pos, level)
    if not moves:
        return pos
    if len(moves) == 1:
        return moves[0]
    if 'last_pos' in memory:
        moves.remove(memory['last_pos'])
    new_pos = random.choice(moves)
    memory['last_pos'] = pos
    return new_pos

