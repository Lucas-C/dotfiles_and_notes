GHOSTINSIGHT_RISKFACTOR = .5
BLOCK_RISK = {
    '#': 0,
    '_': .9,
    '.': .5,
    'X': 0, # shortcircuit: another ghost is way more dangerous right now !
}

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
    return next(any_other_dirs)

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

