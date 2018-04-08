# UNFINISHED: gets stuck in get_door_chains_in_paths for last input: python challenge6.py < chall6/input6.txt
# NOTE: the official solution (in C++ & PHP) use some kind of "flow augmenting" Ford–Fulkerson algorithm to solve this very efficiently :
# https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
import sys
def local_print(*args): print(*args, file=sys.stderr)
from collections import defaultdict
from itertools import permutations
def get_doors_to_close(m):
    ducks = list(list_pos_for_char(m, 'c'))
    if not ducks:
        return []  # no need to close any door
    duck_paths = {duck: build_duck_paths(m, duck) for duck in ducks}
    c = build_constraints(m, duck_paths)
    if not c or not any(_ for _ in c.values()):
        return []  # no duck can attack any patient
    local_print('constraints:', c)
    door_chains = set.union(*sum((list(l.values()) for l in c.values()), []))
    if () in door_chains:
        raise RuntimeError('Some ducks can attack patients but there are no doors to close on their paths !')
    closable_doors = set(sum(door_chains, ()))  # all doors on ducks paths to patients
    local_print('closable doors:', closable_doors)
    for dcount in range(1, len(closable_doors) + 1):
        for doors_to_close in permutations(closable_doors, dcount):
            if constraints_satisfied(c, doors_to_close):
                local_print('doors_to_close:', doors_to_close)
                return doors_to_close
    raise RuntimeError('There is no solution')
def list_pos_for_char(m, target):
    for i, line in enumerate(m):
        for j, c in enumerate(line):
            if c == target:
                yield (i, j)
def build_duck_paths(m, duck):
    paths, explore_stack = defaultdict(set), [duck]
    while explore_stack:
        start = explore_stack.pop(0)
        for pos in nearby_tiles(start, len(m)):
            i, j = pos
            if m[i][j] != '#' and m[i][j] != 'c':
                if pos not in paths and m[i][j] != 'p':
                    explore_stack.append(pos)
                paths[pos].add(start)
    return paths
def build_constraints(m, duck_paths):
    'constraints: c[patient][duck] = set(doors)'
    c = {}
    for patient in list_pos_for_char(m, 'p'):
        c[patient] = {}
        for duck, paths in duck_paths.items():
            if patient in paths:
                c[patient][duck] = get_door_chains_in_paths(patient, paths, m)
    return c
def constraints_satisfied(c, doors_to_close):
    for dp_per_duck in c.values():
        for door_chains in dp_per_duck.values():
            if not all(any(d in doors_to_close for d in doors) for doors in door_chains):
                return False
    return True
def nearby_tiles(pos, N):
    i, j = pos
    if i > 0:
        yield (i - 1, j)
    if i + 1 < N:
        yield (i + 1, j)
    if j > 0:
        yield (i, j - 1)
    if j + 1 < N:
        yield (i, j + 1)
def get_door_chains_in_paths(pos, paths, m, visited=None):
    'Return: set(tuple(doors))'
    i, j = pos
    if m[i][j] == 'c':
        return {()}
    visited = visited | {pos} if visited else {pos}  # this makes a copy of `visited`, so it is shared only by downstream calls
    parent_door_chains = [get_door_chains_in_paths(parent_pos, paths, m, visited)
                          for parent_pos in paths[pos]
                          if parent_pos not in visited]
    parent_door_chains = set.union(*parent_door_chains) if parent_door_chains else set()
    return {(pos,) + dp for dp in parent_door_chains} if m[i][j] == '?' else parent_door_chains
N = int(input())
m = [list(input()) for i in range(N)]  # level map
try:
    print(len(get_doors_to_close(m)))
except RuntimeError as error:
    local_print('Error:', error)
    print(-1)