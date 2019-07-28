#!/usr/bin/python3

# Autonomous runner that does not rely on process stdin/stdout nor threads.
# Re-use the original Runner module functions, but re-implement its main one.
# Does not rely on the original "Answer.py" module, but depends on the *_answer.py modules,
# containing an Answer with a .iteration method

import argparse, importlib, pkg_resources, sys, time

import Runner
from Runner import *


def main_with_defaults():
    '''To be called from zipapp'''
    with pkg_resources.resource_stream(__name__, 'level0.txt') as level_file_bytestream:
        level = [line.decode().strip() for line in level_file_bytestream.readlines()]
    Runner.DEBUG = False
    args = parse_args()
    try:
        main(level, hero_strat_name='my', sleep=args.iteration_sleep)
    except Exception as exception:
        error_msg = exception.__class__.__name__
        if args.explicit:
            error_msg += ': {}'.format(exception)
        print(error_msg, file=sys.stderr)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(prog='BlackBox')
    parser.add_argument('--explicit', action='store_true', help='Makes it easier by providing detailed error messages')
    parser.add_argument('--iteration-sleep', type=float, default=.1, help='Time to sleep between loops')
    return parser.parse_args()
    

def main(level, ia_name_or_path='ia_exploring_and_chasing', hero_strat_name='optimal', sleep=.1):
    ghosts = list(get_ghosts_pos(level))
    ghosts_memory = [{} for _ in ghosts]
    ia = importlib.import_module(ia_name_or_path.split('.')[0])
    dbg_display_level(level)

    init_args = []
    print_cg_init(init_args.append, level)
    hero_strat_module = importlib.import_module(hero_strat_name + '_answer')
    answer = hero_strat_module.Answer(*init_args)

    while True:
        iter_args = []        
        def write_output(*args):
            iter_args.append(' '.join(map(str, args)))
        print_cg_formatted_level(write_output, level, ghosts)
        pacman_dir = answer.iteration(*iter_args)
        if sleep:
            time.sleep(sleep)
        print(pacman_dir, file=sys.stderr)
        move_pacman(level, pacman_dir)
        for i, old_ghost_pos in enumerate(ghosts):
            set_tile(level, old_ghost_pos, '_')
            ghosts[i] = ia.compute_ghost_pos(old_ghost_pos, level, ghosts_memory[i])
            check_pacman_eaten(ghosts[i], level)
            set_tile(level, ghosts[i], 'X')

def test_static_hero_strat():
    import pytest
    with pytest.raises(GameOver):
        main(read_level('level0.txt'), hero_strat_name='static', sleep=None)

def test_empty_hero_strat():
    import pytest
    with pytest.raises(ValueError):
        main(read_level('level0.txt'), hero_strat_name='empty', sleep=None)

def test_go_left_hero_strat():
    import pytest
    with pytest.raises(ValueError):
        main(read_level('level0.txt'), hero_strat_name='go_left', sleep=None)

if __name__ == '__main__':
    main(read_level('level0.txt'))
