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
    dir_change = None
    while True:
        snake, coin = runner.iteration(dir_change)
        if runner.is_game_over():
            break
        kwargs = {'coin': coin} if coin else {}
        dir_change = answer.iteration(*snake, **kwargs)
    print('Congratulations: YOU WIN !')


UP_DIR = (0, 1)
LEFT_DIR = (-1, 0)
DOWN_DIR = (0, -1)
RIGHT_DIR = (1, 0)
DIR_CHANGES = {
    UP_DIR: {'<': LEFT_DIR, '>': RIGHT_DIR},
    LEFT_DIR: {'<': DOWN_DIR, '>': UP_DIR},
    DOWN_DIR: {'<': RIGHT_DIR, '>': LEFT_DIR},
    RIGHT_DIR: {'<': UP_DIR, '>': DOWN_DIR},
}

class Runner:
    def __init__(self, square_size=10, debug=True):
        self.level = [' '*square_size]*square_size
        self.snake = [(randrange(1, square_size - 1), randrange(1, square_size - 1))]
        self._set_tile(self.snake[0], 's')
        self.direction = choice(list(DIR_CHANGES.keys()))
        self.turn_count = 0
        self.coins = []
        self.collected_coin_count = 0
        self.debug = debug
        self.answer_ctor_args = [square_size]
        self.answer_ctor_kwargs = {}
    def iteration(self, dir_change):
        self._debug_print('Dir change:', dir_change)
        if dir_change in DIR_CHANGES[self.direction]:
            self.direction = DIR_CHANGES[self.direction][dir_change]
        self._move_snake()
        self.turn_count += 1
        coin = None
        if self.turn_count % 20 == 0:
            x, y = self.snake[0]
            while self.level[y][x] != ' ':
                x, y = randrange(1, len(self.level) - 1), randrange(0, len(self.level) - 1)
            coin = x, y
            self._set_tile(coin, 'o')
            self.coins.append(coin)
            if len(self.coins) > 3:
                self._set_tile(self.coins.pop(0), ' ')
        self._dbg_display_level()
        return self.snake, coin
    def is_game_over(self):
        return self.collected_coin_count >= 15
    def _move_snake(self):
        # Placing new head one tile further:
        head = self.snake[0]
        x, y = head[0] + self.direction[0], head[1] + self.direction[1]
        max = len(self.level)
        if x < 0 or x >= max or y < 0 or y >= max:
            raise GameOver('Wall hit')
        if self.level[y][x] == 's':
            raise GameOver('Self eaten')
        if self.level[y][x] == 'o':
            self.collected_coin_count += 1
        else:
            self._set_tile(self.snake[-1], ' ')
            self.snake.pop()
        self._set_tile((x, y), 's')
        self.snake.insert(0, (x, y))
    def _set_tile(self, pos, char):
        x, y = pos
        self.level[y] = self.level[y][:x] + char + self.level[y][x+1:]
    def _dbg_display_level(self):
        self._debug_print(' ' + '-'*len(self.level))
        self._debug_print('\n'.join('|'+line+'|' for line in self.level))
        self._debug_print(' ' + '-'*len(self.level))
    def _debug_print(self, *args):
        if self.debug:
            print(*args, file=sys.stderr)

class GameOver(Exception): pass


if __name__ == '__main__':
    main(Runner())
