import sys

from hero_utils import render, allowed_moves_for


def unexplored_dir(hero_pos, moves, level, last_pos):
    # We explore all possible paths, tracking which dir brough us on every tile,
    # and we choose the dir that bring us first to a unexplored place
    visited = set([hero_pos])
    moves_queue_per_dir = {dir: [pos] for dir, pos in moves.items()}
    while sum(1 for dir, moves_queue in moves_queue_per_dir.items() if moves_queue) > 1:
        for dir in moves_queue_per_dir.keys():
            next_moves = []
            for x, y in moves_queue_per_dir[dir]:
                if level[y][x] == '.':
                    return dir
                visited.add((x, y))
                for _, new_pos in allowed_moves_for((x, y), level).items():
                    if new_pos not in visited:
                        next_moves.append(new_pos)
            moves_queue_per_dir[dir] = next_moves
    try:
        return next(dir for dir, moves_queue in moves_queue_per_dir.items() if moves_queue)
    except StopIteration:
        # Means all moves_queues are empty:
        raise WholeLevelExplored()

class WholeLevelExplored(Exception): pass

def test_explorerinstinct():
    assert 282 == _count_steps_before_exploring_all(EMPTY_LVL)

def _count_steps_before_exploring_all(lvl, max_steps=1000):
    level = lvl.splitlines()
    def set_tile(pos, char): x, y = pos; level[y] = level[y][:x] + char + level[y][x+1:]
    hero_pos = next((x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'H')
    last_pos = None
    visited = set([hero_pos])
    for frame in range(max_steps):
        set_tile(hero_pos, '_')
        moves = allowed_moves_for(hero_pos, level)
        unvisited_moves = {dir: pos for dir, pos in moves.items() if pos not in visited}
        if unvisited_moves:
            moves = unvisited_moves
        if len(moves) == 1:
            dir = list(moves.keys())[0]
        else:
            try:
                dir = unexplored_dir(hero_pos, moves, level, last_pos)
            except WholeLevelExplored:
                render(level)
                return frame
        hero_pos, last_pos = moves[dir], hero_pos
        set_tile(hero_pos, 'H')
        visited.add(hero_pos)
    render(level)

EMPTY_LVL = '''\
##############################
#............................#
#.########.########.########.#
#.#......#.#......#.#......#.#
#.#....###.########.##.....#.#
#.#....#.............#.....#.#
#.#....#.###########.#.....#.#
#.######.#.........#.#######.#
#........#.........#.........#
#.######.#.........#.#######.#
#.#....#.####...####.#.....#.#
#.#....#.............#.....#.#
#.#....#.###########.#.....#.#
#.#....#.#.........#.#.....#.#
#.######.###########.#######.#
#............................#
#.######.###########.#######.#
#.######......H......#######.#
#........###########.........#
##########.........###########
'''
