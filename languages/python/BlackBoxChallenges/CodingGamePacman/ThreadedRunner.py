#!/usr/bin/python3

# Thread-based runner using Runner.py
# Currently does not shut down fully in case any error arise (extra CTRL-C are needed)

import pkg_resources
from queue import Queue
from threading import Thread

from Answer import main as answer
from Runner import main as runner, read_level


def main_with_defaults():
    '''To be called from zipapp'''
    with pkg_resources.resource_stream(__name__, 'level0.txt') as level_file_bytestream:
        level = [line.decode().strip() for line in level_file_bytestream.readlines()]
    main(level, 'ia_exploring_and_chasing')

def main(level_filepath='level0.txt', ia_name_or_path='ia_exploring_and_chasing', hero_strat_name='optimal'):
    level = read_level(level_filepath)
    pacman_output_queue = Queue()
    pacman_input_queue = Queue()
    answer_thread = AnswerThread(pacman_input_queue, pacman_output_queue, hero_strat_name)
    runner_thread = RunnerThread(pacman_input_queue, pacman_output_queue, level, ia_name_or_path)
    answer_thread.start()
    runner_thread.start()
    answer_thread.join()
    runner_thread.join()

class RunnerThread(Thread):
    def __init__(self, pacman_input_queue, pacman_output_queue, level, ia_name_or_path):
        Thread.__init__(self)
        self.pacman_input_queue = pacman_input_queue
        self.pacman_output_queue = pacman_output_queue
        self.level = level
        self.ia_name_or_path = ia_name_or_path
    def run(self):
        runner(self.level, self.ia_name_or_path, .1, self.write_output, self.get_pacman_dir)
    def write_output(self, *args):
        self.pacman_input_queue.put(' '.join(map(str, args)))
    def get_pacman_dir(self):
        return self.pacman_output_queue.get()

class AnswerThread(Thread):
    def __init__(self, pacman_input_queue, pacman_output_queue, hero_strat_name):
        Thread.__init__(self)
        self.pacman_input_queue = pacman_input_queue
        self.pacman_output_queue = pacman_output_queue
        self.hero_strat_name = hero_strat_name
    def run(self):
        answer(self.get_input, self.write_output, self.hero_strat_name)
    def get_input(self):
        return self.pacman_input_queue.get()
    def write_output(self, *args):
        self.pacman_output_queue.put(' '.join(map(str, args)))


if __name__ == '__main__':
    main()
