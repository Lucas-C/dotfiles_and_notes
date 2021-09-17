#!/usr/bin/env python3
# Author: Lucas Cimon
# LICENSE: MIT
import resource, sys
from typing import NamedTuple
import gizeh
import moviepy.editor as mpy

W,H = 256,256 # width, height, in pixels
gs = None  # current GameState

def main():
    global gs
    gs = solver(Board.central_european(), goal=2).reverse()
    clip = mpy.VideoClip(make_frame, duration=(gs.depth() - 1)*.5)
    clip.write_gif("peg_solitaire_central_european_solution.gif", fps=2, opt="OptimizePlus", fuzz=10)
    gs = solver(Board.alt_european(), goal=1).reverse()
    clip = mpy.VideoClip(make_frame, duration=(gs.depth() - 1)*.5)
    clip.write_gif("peg_solitaire_alt_european_solution.gif", fps=2, opt="OptimizePlus", fuzz=10)

def dist_to_corner(x, y):  # shortest Manhattan distance to any of the 4 board corners
    return min(x + y, 6-x + y, x + 6-y, 6-x + 6-y)
ALL_POSITIONS = tuple((x, y) for x in range(7) for y in range(7)
                             if dist_to_corner(x, y) > 1)  # european board

class Board(NamedTuple):
    pawns: tuple  # several (x,y) positions
    @classmethod
    def central_european(cls):
        return cls(pawns=tuple(pos for pos in ALL_POSITIONS if pos != (3, 3)))
    @classmethod
    def alt_european(cls):
        return cls(pawns=tuple(pos for pos in ALL_POSITIONS if pos != (3, 2)))
    def __str__(self):
        return '\n'.join(''.join(' ' if dist_to_corner(x, y) <= 1 else ('O' if (x, y) in self.pawns else '.')
                                 for x in range(7))
                         for y in range(7))
    def next_moves(self):
        for pawn in self.pawns:
            x, y = pawn
            for middle_pos, dest_pos in (
                ((x, y-1), (x, y-2)),   # UP
                ((x-1, y), (x-2, y)),   # LEFT
                ((x, y+1), (x, y+2)),   # DOWN
                ((x+1, y), (x+2, y))    # RIGHT
            ):
                is_valid = (middle_pos in ALL_POSITIONS
                        and dest_pos in ALL_POSITIONS
                        and middle_pos in self.pawns
                        and dest_pos not in self.pawns)
                if not is_valid:
                    continue
                new_pawns = tuple(p for p in self.pawns if p not in (pawn, middle_pos)) + (dest_pos,)
                yield pawn, dest_pos, Board(pawns=new_pawns)
    def pawns_symetries(self):
        yield self.pawns
        # Vertical symetry:
        yield tuple((6 - x, y) for (x, y) in self.pawns)
        # Horizontal symetry:
        yield tuple((x, 6 - y) for (x, y) in self.pawns)
        # Central symetry:
        yield tuple((6 - x, 6 - y) for (x, y) in self.pawns)
        # Diagonal symetries:
        yield tuple((y, x) for (x, y) in self.pawns)
        yield tuple((y, 6 - x) for (x, y) in self.pawns)
        yield tuple((6 - y, x) for (x, y) in self.pawns)
        yield tuple((6 - y, 6 - x) for (x, y) in self.pawns)
    def score(self):  # Higher means less dense board
        border = 0
        for x, y in self.pawns:
            for i, j in ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)):
                if (i, j) in ALL_POSITIONS and (i, j) not in self.pawns:
                    border += 1
        return border

class GameState(NamedTuple):
    board: Board
    src_pawn: tuple = None
    dst_pawn: tuple = None
    prev_state: 'GameState' = None
    def depth(self):
        length = 0
        while self:
            self = self.prev_state
            length += 1
        return length
    def reverse(self):
        out_gs = GameState(self.board)
        while self:
            board, src_pawn, dst_pawn, self = self.board, self.src_pawn, self.dst_pawn, self.prev_state
            out_gs = GameState(board, src_pawn, dst_pawn, out_gs)
        return out_gs

def solver(initial_board, goal):
    # Heavily inspired by https://github.com/mkhrapov/peg-solitaire-solver#algorithm
    # & https://github.com/mkhrapov/peg-solitaire-solver/blob/master/src/main/java/org/khrapov/pegsolitaire/solver/Position.java#L213
    # Without this heuristic, I was already removing board symetries but couldn't find a solution with less than 4 remaining pawns.
    pruningNumber = 250
    boards_visited = {hash(initial_board.pawns)}  # storing only hashes to keep the memory usage low
    generation = [GameState(initial_board)]
    while generation:
        next_gen = []
        for gs in generation:
            new_min_reached = False
            for src_pawn, dst_pawn, board in gs.board.next_moves():
                next_gs = GameState(board, src_pawn, dst_pawn, gs)
                if len(board.pawns) == goal:
                    return next_gs
                elif not any(hash(pawns) in boards_visited for pawns in board.pawns_symetries()):
                    boards_visited.add(hash(board.pawns))
                    next_gen.append(next_gs)
        if len(next_gen) > pruningNumber:
            print(f'Pruning generation (heuristic): {len(next_gen)} > {pruningNumber}')
            generation = sorted(next_gen, key= lambda gs: gs.board.score())[:pruningNumber]
        else:
            generation = next_gen
    raise RuntimeError('No solution found!')

def make_frame(t):
    global gs
    if not gs:
        return gizeh.Surface(W, H, bg_color=(255, 0, 0)).get_npimage()
    board, src_pawn, dst_pawn, gs = gs.board, gs.src_pawn, gs.dst_pawn, gs.prev_state
    surface = gizeh.Surface(W, H, bg_color=(255, 255, 255))
    # Draw board:
    for x, y in ALL_POSITIONS:
        fill = (0, 0, 1) if (x, y) in board.pawns else (0, 0, 0)
        gizeh.circle(10, xy=(to_x(x), to_y(y)), fill=fill).draw(surface)
    if src_pawn and dst_pawn:  # Draw "move" arrow:
        x1, y1 = src_pawn
        x2, y2 = dst_pawn
        x, y = (x1 + x2) / 2, (y1 + y2) / 2
        width = abs(x1-x2+.25)*W/8
        height = abs(y1-y2+.25)*H/8
        gizeh.rectangle(lx=width, ly=height, xy=(to_x(x), to_y(y)), fill=(1, 0, 0)).draw(surface)
        x_dir = (x2 - x1) / abs(x2 - x1) if not x1 == x2 else 0  # results in -1 / 0 / +1
        y_dir = (y2 - y1) / abs(y2 - y1) if not y1 == y2 else 0  # results in -1 / 0 / +1
        triangle_pts = (
            (to_x(x2 + x_dir/2),              to_y(y2 + y_dir / 2)),
            (to_x(x2 - x_dir*.25 - y_dir*.5), to_y(y2 - y_dir*.25 - x_dir*.5)),
            (to_x(x2 - x_dir*.25 + y_dir*.5), to_y(y2 - y_dir*.25 + x_dir*.5)),
        )
        gizeh.polyline(triangle_pts, close_path=True, fill=(1, 0, 0)).draw(surface)
    return surface.get_npimage()
def to_x(x):  # scale to canvas
    return (x+1)*W/8
def to_y(y):  # scale to canvas
    return (y+1)*H/8

if __name__ == '__main__':
    main()
