import random

def compute_ghost_pos(pos, level):
    x, y = pos
    moves = [
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
    ]
    max_x, max_y = len(level[0]), len(level)
    for next_pos in list(moves):
        x, y = next_pos
        if x == 0 or x == max_x or y == 0 or y == max_y or level[y][x] == '#':
            moves.remove(next_pos)
    return random.choice(moves)
