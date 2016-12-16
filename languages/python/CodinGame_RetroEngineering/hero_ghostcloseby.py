#!/usr/bin/python3
#--------------------------------------------------------------------------------------------------#
import sys

DIST_WHERE_GHOSTS_ARE_A_POTENTIAL_THREAT = 7
DIST_WHERE_GHOSTS_ARE_A_DEFINITIVE_THREAT = 5

BLOCK_RISK = {
    '#': 0,
    '_': .99, # Not 1 sot that ghosts that are at a further distance get a lower score
    'H': .99, # same as '_'
    '.': .5,
    'X': 0, # shortcircuit: another ghost is way more dangerous right now !
}

def ghosts_are_close_enough_to_worry(pos, ghosts):
    if not ghosts: return False
    return dist_to_closest_ghost(pos, ghosts) <= DIST_WHERE_GHOSTS_ARE_A_DEFINITIVE_THREAT

def dist_to_closest_ghost(pos, ghosts):
    return min(distance(pos, ghost) for ghost in ghosts)

def sum_of_dists_to_ghosts_in_radius(pos, ghosts, radius):
    total = 0
    for ghost in ghosts:
        dist = distance(pos, ghost)
        if dist <= radius:
            print('Adding ghost dist', ghost, dist, file=sys.stderr)
            total += dist
    return total

def distance(posA, posB):
    return (posA[0] - posB[0] if posA[0] > posB[0] else posB[0] - posA[0]) \
        + (posA[1] - posB[1] if posA[1] > posB[1] else posB[1] - posA[1])

def test_dcg():
    assert 2 == dist_to_closest_ghost((0, 0), [(3, 3), (1, 2), (1, 1) , (3, 0)])
    assert 8 == sum_of_dists_to_ghosts_in_radius((0, 0), [(3, 3), (1, 2), (1, 1) , (3, 0)], 3)



def safest_move(pos, moves, ghosts, level):
    close_ghosts = [g for g in ghosts if distance(pos, g) <= DIST_WHERE_GHOSTS_ARE_A_POTENTIAL_THREAT]
    risk_factors = sorted([(risk_factor(move[1], ghosts, level, close_ghosts), move) for move in moves.items()])
    moves_sorted_by_safest = sorted(risk_factors, key=lambda e: e[0][0] - e[0][1])
    print('GhostCloseby! Moves sorted by risk factors:', moves_sorted_by_safest, file=sys.stderr)
    return moves_sorted_by_safest[0][1]

def risk_factor(pos, ghosts, level, close_ghosts):
    sum_of_dists_to_close_ghosts = sum(distance(pos, g) for g in close_ghosts)
    return get_riskiest_gis(pos, ghosts, level)[0], sum_of_dists_to_close_ghosts


def test_sm():
    dir_akas = {'A': 'right', 'E': 'left', 'C': 'up', 'D': 'down'}
    lvl = '''\
.#.
H#.
.X.
'''
    print(lvl)
    safest_move = _sm_from_level(lvl)
    dir_aka = dir_akas[safest_move[0]]
    print('Safest dir:', dir_aka)
    assert ('up', (0, 0)) == (dir_aka, safest_move[1])
    lvl = '''\
..X.
.H#.
...X
'''
    print(lvl)
    safest_move = _sm_from_level(lvl)
    dir_aka = dir_akas[safest_move[0]]
    print('Safest dir:', dir_aka)
    assert ('left', (0, 1)) == (dir_aka, safest_move[1])


def _sm_from_level(level_str):
    level = level_str.splitlines()
    hero = next((x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'H')
    moves = _sm_allowed_moves_for(hero, level)
    ghosts = [(x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'X']
    return safest_move(hero, moves, ghosts, level)

def _sm_allowed_moves_for(pos, level):
    x, y = pos
    moves = {
        'C': (x, y - 1), # up
        'A': (x + 1, y), # right
        'D': (x, y + 1), # down
        'E': (x - 1, y), # left
    }
    for dir in _sm_get_blocked_dirs(list(moves.items()), level):
        del moves[dir]
    return moves

def _sm_get_blocked_dirs(dir_pos_pairs, level):
    max_x, max_y = len(level[0]), len(level)
    for dir, pos in dir_pos_pairs:
        x, y = pos
        if x < 0 or x >= max_x or y < 0 or y >= max_y or level[y][x] == '#':
            yield dir



def get_riskiest_gis(hero_pos, ghosts, level):
    return max((ghost_in_sight_risk(hero_pos, ghost, level), ghost) for ghost in ghosts)

def get_aligned_pos_dir(src, dst):
    assert src != dst
    if src[0] == dst[0]:
        return 'C' if dst[1] < src[1] else 'D'
    elif src[1] == dst[1]:
        return 'A' if dst[0] > src[0] else 'E'
    else:
        raise ValueError('Positions are not aligned')

def select_escape_dir(moves, dir):
    horiz_dirs = ['A', 'E']
    verti_dirs = ['C', 'D']
    if dir in horiz_dirs:
        horiz_dirs.remove(dir)
        opposite_dir = horiz_dirs[0]
    else:
        verti_dirs.remove(dir)
        opposite_dir = verti_dirs[0]
    if opposite_dir in moves:
        return opposite_dir
    any_other_dirs = sorted(d for d in moves if d != dir)
    return any_other_dirs[0]

def ghost_in_sight_risk(hero_pos, ghost, level):
    """
    Returns a score between 0 & 1 indicating the probability that a ghost has a straight line of sight to the hero
    """
    risk = 1
    if ghost[0] == hero_pos[0]:
        x = hero_pos[0]
        for y in intermediate_positions(hero_pos[1], ghost[1]):
            risk *= BLOCK_RISK[level[y][x]]
        return risk
    elif ghost[1] == hero_pos[1]:
        y = hero_pos[1]
        for x in intermediate_positions(hero_pos[0], ghost[0]):
            risk *= BLOCK_RISK[level[y][x]]
        return risk
    else:
        return 0

def intermediate_positions(src, dst):
    if src < dst:
        yield from range(src + 1, dst)
    else:
        yield from range(src - 1, dst, -1)


def test_gis():
    _gis_test_runner('H__X', (BLOCK_RISK['_']**2, (3, 0)))
    _gis_test_runner('H...X', (BLOCK_RISK['.']**3, (4, 0)))
    _gis_test_runner('H\n_\nX', (BLOCK_RISK['_'], (0, 2)))

def _gis_test_runner(lvl, expected):
    print(lvl)
    level = lvl.splitlines()
    hero = next((x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'H')
    ghosts = [(x, y) for y, line in enumerate(level) for x in range(len(line)) if level[y][x] == 'X']
    assert expected == get_riskiest_gis(hero, ghosts, level)

