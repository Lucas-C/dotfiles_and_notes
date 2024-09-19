#!/usr/bin/env python3
# From PagedOut #4 page 32 - https://alperenkeles.com/blog/paintbrush
# USAGE: ./paintbrush.py
# RUN TESTS: pytest paintbrush.py
import math
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from heapq import heappush, heappop
from itertools import product
from string import ascii_uppercase
from textwrap import dedent


MAX_SIZE = 256  # maximum canva size


class C(Enum):
    "Color"
    RED = "RED"
    BLUE = "BLUE"

class D(Enum):
    "Direction"
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"

@dataclass
class Brush:
    name: str
    dir: D
    k: int  # row or column index
    def color(self):
        return C.RED if self.dir is D.HORIZONTAL else C.BLUE

@dataclass
class Canva:
    grid : list(list(C))
    @classmethod
    def from_string(cls, text):
        return cls([[C.RED if c == 'R' else C.BLUE for c in row]
                    for row in dedent(text).strip().splitlines()])
    @property
    def column_count(self):
        return len(self.grid[0])
    @property
    def row_count(self):
        return len(self.grid)
    def __hash__(self):
        h = 0
        for row in self.grid:
            for c in row:
                h += 1 if c is C.RED else 0
                h *= 2
        # assert self.column_count == self.row_count
        # assert self.row_count < MAX_SIZE
        return h * MAX_SIZE + self.row_count
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __gt__(self, other):
        return hash(self) > hash(other)
    def __str__(self):
        return '\n'.join(''.join('R' if c is C.RED else 'B' for c in row) for row in self.grid)
    def columns(self):
        for j in range(self.column_count):
            yield [row[j] for row in self.rows()]
    def rows(self):
        return self.grid
    def copy(self):
        return self.__class__([list(row) for row in self.grid])
    def copy_with_column(self, column, j):
        copy = self.copy()
        for i, row in enumerate(copy.grid):
            row[j] = column[i]
        return copy
    def copy_with_row(self, row, i):
        copy = self.copy()
        copy.grid[i] = row
        return copy
    def brush_name(self, i=None, j=None):
        return ascii_uppercase[i] if i is not None else ascii_uppercase[self.row_count + j]
    def apply_brush(self, brush):
        if brush.dir is D.HORIZONTAL:
            return self.copy_with_row([brush.color()] * self.column_count, i=brush.k)
        else:
            return self.copy_with_column([brush.color()] * self.row_count, j=brush.k)
    def prev_brushes(self):
        """
        Iterate over all possible immediate previous brushes
        that could have been applied to lead to the current canva.
        """
        for i, row in enumerate(self.rows()):
            if row.count(C.BLUE) == 0:
                yield Brush(self.brush_name(i=i), dir=D.HORIZONTAL, k=i)
        for j, column in enumerate(self.columns()):
            if column.count(C.RED) == 0:
                yield Brush(self.brush_name(j=j), dir=D.VERTICAL, k=j)
    def is_solvable(self):
        """
        This is a required condition,
        but does not really ensure that the grid has a solution.
        """
        return len(list(self.prev_brushes())) > 0
    def prev_canvas(self, brush):
        """
        Iterate over all possible immediate previous canvas
        that could be transformed by a given brush into the current one.
        """
        if brush.dir is D.HORIZONTAL:
            current_row = tuple(self.grid[brush.k])
            for row in product((C.RED, C.BLUE), repeat=self.column_count):
                if row != current_row:
                    yield self.copy_with_row(list(row), i=brush.k)
        else:
            current_column = tuple(row[brush.k] for row in self.grid)
            for column in product((C.RED, C.BLUE), repeat=self.row_count):
                if column != current_column:
                    yield self.copy_with_column(column, j=brush.k)
    def prev_brush_and_canvas(self):
        for brush in self.prev_brushes():
            for prev_canva in self.prev_canvas(brush):
                yield brush, prev_canva
    def similarity_score(self, other_canva):
        """
        Compute a score between 0 & 1
        where 0 means totally distincts
        and 1 means totally identical
        """
        assert self.column_count == other_canva.column_count
        assert self.row_count == other_canva.row_count
        score = 0
        for row, o_row in zip(self.rows(), other_canva.rows()):
            for cell, o_cell in zip(row, o_row):
                if cell == o_cell:
                    score += 1
        return score / self.column_count / self.row_count
    def brushes_to(self, dst_canva):
        "A* pathfinding algorithm"
        priority_queue = []
        #                             score, #steps-to-reach-dst_canva, canva
        heappush(priority_queue, (-self.similarity_score(dst_canva), 0, dst_canva))
        prev = {}  # map canva to (prev_canva, prev_brush)
        # For node C, score[C] is the cost of the cheapest path from start to C currently known.
        score = defaultdict(lambda: math.inf)
        score[dst_canva] = 0
        # def brushes_from(canva):
        #     out = ""
        #     while canva != dst_canva:
        #         canva, brush = prev[canva]
        #         out += brush.name
        #     return out
        while priority_queue:
            _score, steps, cur_canva = heappop(priority_queue)
            # print(f"Considering canva with hash {hash(cur_canva)} & score {_score:.2f} at step {steps} before brushes {brushes_from(cur_canva)}:\n{cur_canva}")
            if cur_canva == self:
                while cur_canva != dst_canva:
                    cur_canva, prev_brush = prev[cur_canva]
                    yield prev_brush
                return
            for brush, prev_canva in cur_canva.prev_brush_and_canvas():
                similarity = self.similarity_score(prev_canva)
                tentative_score = -similarity
                # print(f"* brush: {brush.name} / hash(canva): {hash(prev_canva)} ? score={tentative_score:.2f} < prev_score={score[prev_canva]:.2f}")
                if tentative_score < score[prev_canva]:
                    prev[prev_canva] = cur_canva, brush
                    score[prev_canva] = tentative_score
                    heappush(priority_queue, (tentative_score + steps, steps + 1, prev_canva))
        raise RuntimeError("No solution found")


def test_equal():
    assert Canva([[C.RED]]) == Canva([[C.RED]])
    assert Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]) == Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ])

def test_apply_brush():
    assert Canva([[C.BLUE]]).apply_brush(Brush('A', D.HORIZONTAL, 0)) == Canva([[C.RED]])
    assert Canva([[C.RED]]).apply_brush(Brush('B', D.VERTICAL, 0)) == Canva([[C.BLUE]])
    assert Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]).apply_brush(Brush('A', D.HORIZONTAL, 0)) == Canva([
        [C.RED, C.RED],
        [C.RED, C.BLUE]
    ])

def test_is_solvable():
    assert Canva([[C.RED]]).is_solvable()
    assert Canva([[C.BLUE]]).is_solvable()
    assert Canva([
        [C.RED, C.RED],
        [C.RED, C.BLUE]
    ]).is_solvable()
    assert not Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]).is_solvable()

def test_similarity_score():
    assert Canva([[C.BLUE]]).similarity_score(Canva([[C.RED]])) == 0
    assert Canva([[C.RED]]).similarity_score(Canva([[C.RED]])) == 1
    assert Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]).similarity_score(Canva([
        [C.RED, C.RED],
        [C.RED, C.BLUE]
    ])) == .75

def test_prev_canvas_2x2_horizontal():
    canva = Canva([
        [C.RED, C.RED],
        [C.RED, C.BLUE]
    ])
    brush = Brush('A', D.HORIZONTAL, 0)
    prev_canvas = list(canva.prev_canvas(brush))
    assert canva not in prev_canvas
    assert Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]) in prev_canvas
    assert Canva([
        [C.RED, C.BLUE],
        [C.RED, C.BLUE]
    ]) in prev_canvas
    assert Canva([
        [C.BLUE, C.BLUE],
        [C.RED, C.BLUE]
    ]) in prev_canvas
    assert len(set(prev_canvas)) == 3

def test_prev_canvas_2x2_vertical():
    canva = Canva([
        [C.BLUE, C.RED],
        [C.BLUE, C.BLUE]
    ])
    brush = Brush('D', D.VERTICAL, 0)
    prev_canvas = list(canva.prev_canvas(brush))
    assert canva not in prev_canvas
    assert Canva([
        [C.BLUE, C.RED],
        [C.RED, C.BLUE]
    ]) in prev_canvas
    assert Canva([
        [C.RED, C.RED],
        [C.BLUE, C.BLUE]
    ]) in prev_canvas
    assert Canva([
        [C.RED, C.RED],
        [C.RED, C.BLUE]
    ]) in prev_canvas
    assert len(set(prev_canvas)) == 3


if __name__ == "__main__":
    src_canva = Canva([
        [C.BLUE, C.BLUE, C.RED],
        [C.BLUE, C.RED, C.RED],
        [C.RED, C.BLUE, C.BLUE],
    ])
    dst_canva = Canva([
        [C.BLUE, C.RED, C.BLUE],
        [C.BLUE, C.RED, C.RED],
        [C.BLUE, C.BLUE, C.BLUE],
    ])
    c = src_canva
    print(c)  #, "hash:", hash(c))
    for brush in src_canva.brushes_to(dst_canva):
        print("Applying:", brush.name)
        c = c.apply_brush(brush)
        print(c)  #, "hash:", hash(c))
