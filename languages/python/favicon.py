from contextlib import closing
from itertools import chain
from gifmaze import GIFSurface, PixelCanvas, Animation
# This script does not use the current publish version of gifmaze, but the one maintained by Zhao Liang
# cf. https://github.com/neozhaoliang/pywonderland/issues/17

WIDTH, HEIGHT = 16, 16
BOARD = set(((1, 0), (2, 1), (0, 2), (1, 2), (2, 2)))  # Game of Life glider

def next_board(board):
    'Implementation inspired by: https://github.com/erikrose/conway/blob/master/bin/conway.py#L105'
    new_board = set()
    # We need to consider only the points that are alive and their neighbors:
    for point in board | set(chain(*map(neighbors, board))):
        count = sum((neigh in board) for neigh in neighbors(point))
        if count == 3 or (count == 2 and point in board):
            new_board.add(point)
    return new_board
def neighbors(pt):
    'Return the neighbors of a point, with torroidal geometry'
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx != 0 or dy != 0:
                yield (pt[0] + dx) % WIDTH, (pt[1] + dy) % HEIGHT

with closing(GIFSurface(width=WIDTH, height=HEIGHT)) as surface:
    surface.set_palette(
        [0, 0, 0]        # black
      + [255, 255, 255]  # white
      + [255, 0, 0]      # red
      + [0, 255, 0]      # green
      + [0, 0, 255]      # blue
      + [255, 255, 0]    # yellow
      + [0, 255, 255]    # cyan
      + [255, 0, 255]    # magenta
    )

    def favicon(pcanvas, render, board):
        for _ in range(64):
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    pcanvas.set_pixel(x, y, 1 if (x, y) in board else 0)  # last param is a color palette index
            yield render(pcanvas)
            board = next_board(board)
    Animation(surface).run(board=BOARD, algo=favicon, pcanvas=PixelCanvas(width=WIDTH, height=HEIGHT, grid_init=1), delay=7)

    surface.save('favicon.gif')
