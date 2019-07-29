#!/usr/bin/python3

import argparse, importlib, os.path, pkg_resources, sys


def main_with_defaults():
    '''To be called from zipapp'''
    with pkg_resources.resource_stream(__name__, 'level0.txt') as level_file_bytestream:
        level = [line.decode().strip() for line in level_file_bytestream.readlines()]
    args = parse_args()
    if not os.path.exists(args.answercode_filepath):
        raise ValueError('Python answer not found - file does not exists: ' + args.answercode_filepath)
    try:
        main(Runner(level, debug=False), answercode_filepath=args.answercode_filepath)
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
    dirname, basename = os.path.split(answercode_filepath)
    sys.path.insert(0, dirname)
    modulename, _ = os.path.splitext(basename)
    answer_module = importlib.import_module(modulename)
    answer = answer_module.Answer(*runner.answer_ctor_args, **runner.answer_ctor_kwargs)
    car_dir = ''
    while True:
        line = runner.iteration(car_dir)
        if runner.race_is_over:
            break
        car_dir = answer.iteration(line)
    print('Congratulations: YOU WIN !')


class Runner:
    def __init__(self, level, sight_range=5, debug=True):
        self.race_is_over = False
        self.level = level
        self.sight_range = sight_range
        self.line_index = 0
        self.debug = debug
        self.dbg_display_level(self.level)
        self.answer_ctor_args = [self.line2digits(l) for l in self.level[:self.sight_range]]
        self.answer_ctor_kwargs = {'position': self.car_pos_x()}
    def car_pos_x(self):
        return self.level[self.line_index].index('v')
    def iteration(self, car_dir):
        if self.line_index + 2 == len(self.level):
            self.race_is_over = True
            return
        self.debug_print('Line index:', self.line_index)
        line_in_sight_index = self.line_index + self.sight_range
        self.move_car(car_dir)
        self.dbg_display_level(self.level[self.line_index-1:line_in_sight_index], start_pos=self.line_index-1)
        line_in_sight_info = self.line2digits(self.level[line_in_sight_index]) if line_in_sight_index < len(self.level) else []
        self.debug_print('Sending line info:', line_in_sight_info)
        return line_in_sight_info
    def line2digits(self, line):
        digits = []
        is_wall = line[0] == '#'
        count = 1
        for i in range(1, len(line)):
            if (is_wall and line[i] == '#') or (not is_wall and line[i] != '#'):  # basically a XOR
                count += 1
            else:
                digits.append(count)
                is_wall = not is_wall
                count = 1
        digits.append(count)
        return digits
    def move_car(self, dir):
        old_car_pos_x = self.car_pos_x()
        if dir == '<':
            new_car_pos_x = old_car_pos_x - 1
        elif dir == '>':
            new_car_pos_x = old_car_pos_x + 1
        else:
            new_car_pos_x = old_car_pos_x
        self.line_index += 1
        if self.level[self.line_index][new_car_pos_x] == '#':
            raise GameOver('Crash accident !')
        self.set_tile((old_car_pos_x, self.line_index - 1), ' ')
        self.set_tile((new_car_pos_x, self.line_index), 'v')
    def set_tile(self, pos, char):
        x, y = pos
        self.level[y] = self.level[y][:x] + char + self.level[y][x+1:]
    def dbg_display_level(self, level_portion, start_pos=0):
        self.debug_print('\n'.join('{:2d}:{}'.format(start_pos + i, line) for i, line in enumerate(level_portion)))
    def debug_print(self, *args):
        if self.debug:
            print(*args, file=sys.stderr)

class GameOver(Exception): pass

def read_level(level_filename):
    with open(level_filename) as level_file:
        return [line.strip() for line in level_file.readlines()]


if __name__ == '__main__':
    main(Runner(read_level('level0.txt')))
