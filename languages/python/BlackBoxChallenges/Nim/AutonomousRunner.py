#!/usr/bin/python3

import argparse, importlib, os, os.path, pkg_resources, sys
from random import choice, randrange, seed


def main_with_defaults():
    '''To be called from zipapp'''
    args = parse_args()
    if not os.path.exists(args.answercode_filepath):
        raise ValueError('Python answer not found - file does not exists: ' + args.answercode_filepath)
    try:
        main(Runner(debug=False), answercode_filepath=args.answercode_filepath)
    except Exception as exception:
        error_msg = exception.__class__.__name__
        if args.explicit:
            error_msg += ': {}'.format(exception)
        print(error_msg, file=sys.stderr)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(prog='BlackBox')
    parser.add_argument('--explicit', action='store_true', help='Makes it easier by displaying exceptions detailed messages')
    parser.add_argument('--answercode-filepath', default='answer.py', help='Absolute or relative path to the Python source code of the answer')
    return parser.parse_args()
    

def main(runner, answercode_filepath='answer.py'):
    if 'SEED' in os.environ:
        seed(int(os.environ['SEED']))
    dirname, basename = os.path.split(answercode_filepath)
    sys.path.insert(0, dirname)
    modulename, _ = os.path.splitext(basename)
    answer_module = importlib.import_module(modulename)
    answer = answer_module.Answer(*runner.answer_ctor_args, **runner.answer_ctor_kwargs)
    amount = None
    while not runner.answer_won:
        picked = answer.iteration(amount or runner.amount)
        amount = runner.iteration(picked)
    print('Congratulations: YOU WIN !')


class Runner:
    SENTINEL = object()
    def __init__(self, debug=True):
        self.answer_won = False
        self.amount = 0
        # We ensure the player has an initial chance to win:
        while self.amount % 4 == 0:
            self.amount = randrange(15, 32)
        self.debug = debug
        self.answer_ctor_args = []
        self.answer_ctor_kwargs = {}
    def iteration(self, picked):
        if picked is not self.SENTINEL: 
            if not (1 <= picked <= 3):
                raise GameOver('Invalid amount')
            self.amount -= picked
        if self.amount == 0:
            self.answer_won = True
            return
        if self.amount <= 3:
            raise GameOver('Your opponent won')
        if self.amount % 4 != 0:
            # Optimal strategy:
            runner_pick = self.amount - 4 * (self.amount // 4)
        else:
            runner_pick = randrange(1, 4)
        self._debug_print('Answer pick:', picked, '- Amount: ', self.amount, '- Runner pick: ', runner_pick)
        self.amount -= runner_pick
        return self.amount
    def _debug_print(self, *args):
        if self.debug:
            print(*args, file=sys.stderr)

class GameOver(Exception): pass


if __name__ == '__main__':
    main(Runner())
