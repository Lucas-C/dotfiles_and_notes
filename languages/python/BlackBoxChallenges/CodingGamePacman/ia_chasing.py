# This IA:
# - abide the movement rules
# - chase a hero if it is in sight
# - else choose a random next position, that is NOT its previous one

import random
from ia_utils import get_allowed_moves, iter_coords

def compute_ghost_pos(pos, level, memory):
    moves = get_allowed_moves(pos, level)
    if not moves:
        return pos
    memory['last_pos'] = pos
    if len(moves) == 1:
        return moves[0]
    for move in moves:
        for x, y in iter_coords(pos, move, level):
            if level[y][x] == 'H':
                return move
    if 'last_pos' in memory and memory['last_pos'] in moves:
        moves.remove(memory['last_pos'])
    new_pos = random.choice(moves)
    return new_pos

