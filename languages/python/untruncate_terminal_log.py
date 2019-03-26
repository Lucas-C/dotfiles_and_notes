#!/usr/bin/env python3
# USAGE: untruncate_terminal_log.py --in-place --insert-missing-eol-space tmux_history_2019-03-11-15-33
# Very useful for tmux logs exports that are truncated after 80th char

import argparse, json, sys
from os.path import exists


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('truncated_filepath', help=' ')
    parser.add_argument('--width', type=int, default=80, help=' ')
    parser.add_argument('--insert-missing-eol-space', action='store_true', help=' ')
    parser.add_argument('--in-place', action='store_true', help=' ')
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.truncated_filepath) as truncated_file:
        lines = [l[:-1] for l in truncated_file.readlines()]
    i = 0
    while i + 1 < len(lines):
        if args.insert_missing_eol_space and (len(lines[i]) % args.width) == args.width - 1:
            lines[i] += ' '
        while len(lines[i]) % args.width == 0:
            lines[i] += lines[i + 1]
            del lines[i + 1]
        i += 1
    if args.in_place:
        with open(args.truncated_filepath, 'w') as truncated_file:
            for line in lines:
                truncated_file.write(line + '\n')
    else:
        for line in lines:
            print(line)

if __name__ == '__main__':
    main()
