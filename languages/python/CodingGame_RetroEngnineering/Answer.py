import sys

Y = int(input())
X = int(input())
Z = int(input())
print('INIT:', X, Y, Z, file=sys.stderr)

level = ['.'*X]*Y
visited = set()

def update_level(pacman_pos, neighbours, new_ghosts_pos):
    for pos in get_ghosts_pos():
        set_tile(pos, '_')
    for pos in new_ghosts_pos:
        set_tile(pos, 'X')
    set_tile(pacman_pos, 'H')
    x, y = pacman_pos
    set_tile((x, y - 1), neighbours[0])  # block above
    set_tile((x + 1, y), neighbours[1])  # block on the right
    set_tile((x, y + 1), neighbours[2])  # block below
    set_tile((x - 1, y), neighbours[3])  # block on the left

def set_tile(pos, char):
    x, y = pos
    level[y] = level[y][:x] + char + level[y][x+1:]

def get_ghosts_pos():
    for y, line in enumerate(level):
        for x in range(len(line)):
            if line[x] == 'X':
                yield x, y

def render():
    for y in range(Y):
        for x in range(X):
            print(level[y][x], end='', file=sys.stderr)
        print('', file=sys.stderr)

def choose_dir(pos):
    x, y = pos
    moves = {
        'C': (x, y - 1), # up
        'A': (x + 1, y), # right
        'D': (x, y + 1), # down
        'E': (x - 1, y), # left
    }
    # we remove blocked tiles from the choices
    for dir, pos in list(moves.items()):
        x, y = pos
        if x == 0 or x == X or y == 0 or y == Y or level[y][x] == '#':
            del moves[dir]
    # `moves` cannot be empty at this point (or else pacman started between 4 walls)
    for dir, pos in sorted(moves.items()):
        if pos not in visited:
            return dir, pos
    return sorted(moves.items())[0]

while True:
    print('A: Waiting for neighbours', file=sys.stderr)
    neighbours = [input(), input(), input(), input()]
    print('A: Neighbours read', file=sys.stderr)
    #print(*neighbours, file=sys.stderr)
    coords = []
    print('A: Waiting for Runner coords', file=sys.stderr)
    for _ in range(Z):
        coords.append([int(i) for i in input().split()])
    print('A: Coords read', file=sys.stderr)
    #print(coords, file=sys.stderr)
    pacman_pos, ghosts_pos = coords[-1], coords[:-1]
    update_level(pacman_pos, neighbours, ghosts_pos)
    render()
    dir, new_pos = choose_dir(pacman_pos)
    print(dir)
    set_tile(pacman_pos, '_')
    visited.add(new_pos)

