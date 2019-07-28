# This IA:
# - abide the movement rules
# - chase a hero if it is in sight
# - else choose a next position:
#   1. that is NOT its previous one
#   2. with a preference for lesser visited ones

from collections import defaultdict
from ia_utils import get_allowed_moves, iter_coords

def compute_ghost_pos(pos, level, memory):
    visits_count = memory.setdefault('visits_count', defaultdict(lambda: 0))
    moves = get_allowed_moves(pos, level)
    if not moves:
        visits_count[pos] += 1
        return pos
    memory['last_pos'] = pos
    if len(moves) == 1:
        visits_count[moves[0]] += 1
        return moves[0]
    for move in moves:
        for x, y in iter_coords(pos, move, level):
            if level[y][x] == 'H':
                visits_count[move] += 1
                return move
    if 'last_pos' in memory and memory['last_pos'] in moves:
        moves.remove(memory['last_pos'])
    def sort_key(pos):
        return visits_count.get(pos, 0)
    new_pos = sorted(moves, key=sort_key)[0]
    visits_count[new_pos] += 1
    return new_pos

