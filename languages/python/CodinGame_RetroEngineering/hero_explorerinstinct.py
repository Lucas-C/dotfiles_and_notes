import sys

def unexplored_dir(moves, level, last_pos):
    print('ExplorationMode!', file=sys.stderr)
    # DO NOT GO BACK!
    if last_pos in moves.values():
        moves = {dir: pos for dir, pos in moves.items() if pos != last_pos}
    exploration_scores = {dir: compute_exploration_score(dir, move, level) for dir, move in moves.items()}
    for dir, move in moves.items():
        dir_aka = {'A': 'right', 'E': 'left', 'C': 'up', 'D': 'down'}[dir]
        print('{} ({}): {}'.format(dir, dir_aka, exploration_scores[dir]), file=sys.stderr)
    def sort_key(move):
        dir = move[0]
        return (-exploration_scores[dir], dir)
    return sorted(moves.items(), key=sort_key)[0]

def compute_exploration_score(dir, pos, level):
    should_pos_count = should_pos_count_builder(dir, pos)
    score = 0
    for y, line in enumerate(level):
        for x in range(len(line)):
            if should_pos_count((x, y)):
                if level[y][x] == '.':
                    score += 1
    return score

def should_pos_count_builder(dir, center):
    def should_pos_count(pos):
        rel_x = pos[0] - center[0]
        rel_y = pos[1] - center[1]
        if dir == 'A':    # right
            if rel_x <= 0:
                return False
            return -rel_x < rel_y <= rel_x
        elif dir == 'E':  # left
            if rel_x >= 0:
                return False
            return rel_x <= rel_y < -rel_x
        elif dir == 'D':  # down
            if rel_y <= 0:
                return False
            return -rel_y <= rel_x < rel_y
        elif dir == 'C':  # up
            if rel_y >= 0:
                return False
            return rel_y < rel_x <= -rel_y
    return should_pos_count


def test_ei():
    _ei_test_runner('#.\n.X', expect={'right': 0, 'left': 1, 'up': 1, 'down': 0})
    _ei_test_runner('...\n.X.\n...', expect={'right': 2, 'left': 2, 'up': 2, 'down': 2})
    _ei_test_runner('X..\n...\n...', expect={'right': 5, 'left': 0, 'up': 0, 'down': 3})
    _ei_test_runner('.....\n.....\n.....\n...X.\n.....', expect={'right': 2, 'left': 11, 'up': 9, 'down': 2})
    assert 42 == _ei_count_steps_before_exploring_all(EMPTY_LVL)

def _ei_test_runner(level_str, expect):
    level = level_str.splitlines()
    X, Y = len(level[0]), len(level)
    center = next((x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'X')
    print('> {}x{} - center: {}\n{}'.format(X, Y, center, level_str))
    for dir_aka, expected_count in expect.items():
        dir = {'right': 'A', 'left': 'E', 'up': 'C', 'down': 'D'}[dir_aka]
        count = compute_exploration_score(dir, center, level)
        print('dir: {} ({}) -> count: {}'.format(dir, dir_aka, count))
        assert count == expected_count
    print()
    assert level_str.count('.') == sum(expect.values())

def _ei_count_steps_before_exploring_all(lvl, max_steps=1000):
    level = lvl.splitlines()
    from hero_utils import render, allowed_moves_for
    def set_tile(pos, char): x, y = pos; level[y] = level[y][:x] + char + level[y][x+1:]
    hero_pos = next((x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'H')
    last_pos = None
    for frame in range(max_steps):
        set_tile(hero_pos, '_')
        moves = allowed_moves_for(hero_pos, level)
        hero_pos, last_pos = unexplored_dir(moves, level, last_pos)[1], hero_pos
        set_tile(hero_pos, 'H')
        if sum(row.count('.') for row in level) == 0:
            return frame
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
