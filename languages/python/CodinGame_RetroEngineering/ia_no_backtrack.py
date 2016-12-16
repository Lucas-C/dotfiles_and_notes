# This IA:
# - abide the movement rules
# - choose a random next position, that is NOT its previous one

import random
from ia_utils import adjacent_moves, get_blocked_coords

def compute_ghost_pos(pos, level, memory):
    moves = adjacent_moves(pos)
    for blocked_pos in get_blocked_coords(list(moves), level):
        moves.remove(blocked_pos)
    if not moves:
        return pos
    if len(moves) == 1:
        return moves[0]
    if 'last_pos' in memory:
        moves.remove(memory['last_pos'])
    new_pos = random.choice(moves)
    memory['last_pos'] = pos
    return new_pos

