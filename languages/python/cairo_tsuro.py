#!/usr/bin/env python3
# USAGE: ./this.py [connected]
import cairo, contextlib, math, sys
from itertools import combinations, zip_longest

ROW_LENGTH = 12
if len(sys.argv) > 1 and sys.argv[1] == 'connected':
    VERTEX_COORD = {
        'a': (1, .333),
        'b': (1, .666),
        'c': (.666, 1),
        'd': (.333, 1),
        'e': (0, .666),
        'f': (0, .333),
        'g': (.333, 0),
        'h': (.666, 0),
    }
else:
    VERTEX_COORD = {
        'a': (.9, .333),
        'b': (.9, .666),
        'c': (.666, .9),
        'd': (.333, .9),
        'e': (.1, .666),
        'f': (.1, .333),
        'g': (.333, .1),
        'h': (.666, .1),
    }

def main():
    with image_generator('cairo_tsuro.png', tile_edge=64, width=800, height=600) as context:
        draw_grid(context)
        x, y = 0, 0
        known_tiles = dict()
        for i, tile in enumerate(iter_tiles()):
            known_homotetic_tile = next((t for t in homotetic_tiles(tile) if t in known_tiles), None)
            if known_homotetic_tile:
                is_duplicate = True
                known_tiles[known_homotetic_tile] += 1
            else:
                is_duplicate = False
                known_tiles[tile] = 1
            print (i, tile, '(duplicate)' if is_duplicate else '')
            draw_tile(context, x, y, tile, is_duplicate)
            x += 1
            if x == ROW_LENGTH:
                x = 0
                y += 1
        print('Unique tiles count:', len(known_tiles))

def iter_tiles():
    """Iterate through all the possible tiles so that their normalized form is processed only once"""
    for p1_v2 in 'bcdefgh':
        p1 = 'a', p1_v2
        remaining_vertices_2 = set([v for v in 'bcdefgh' if v != p1_v2])
        for p2 in combinations(sorted(remaining_vertices_2), 2):
            remaining_vertices_3 = remaining_vertices_2 - set(p2)
            for p3 in combinations(sorted(remaining_vertices_3), 2):
                p4 = tuple(sorted(remaining_vertices_3 - set(p3)))
                tile = ''.join(p1 + p2 + p3 + p4)
                if is_normalized(tile):
                    yield tile

def homotetic_tiles(tile):
    "Iterate through the 3 possible rotations of the tile"
    for i in range(3):
        translator = str.maketrans('cdefghab', 'abcdefgh')
        tile = normalize(''.join(tile[2:8] + tile[0:2]).translate(translator))
        yield tile

def is_normalized(tile):
    return tile == normalize(tile)

def normalize(tile):
    return ''.join(sorted([''.join(sorted(p)) for p in grouper(tile, 2)]))

def draw_tile(context, x, y, tile, is_duplicate=False):
    context.set_source_rgb(1 if is_duplicate else 0, 0, 1)
    context.set_line_width(.1)
    for v1, v2 in grouper(tile, 2):
        v1_x, v1_y = VERTEX_COORD[v1]
        v2_x, v2_y = VERTEX_COORD[v2]
        v1_x += x
        v1_y += y
        v2_x += x
        v2_y += y
        context.move_to(v1_x, v1_y)
        context.line_to(v2_x, v2_y)
        context.stroke()
    context.set_source_rgb(1, 0, 0)
    for _, (cx, cy) in VERTEX_COORD.items():
        context.arc(cx + x, cy + y, .05, 0, 2 * math.pi)  # (cx, cy, radius, start_angle, stop_angle)
        context.fill()

def draw_grid(context):
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(.02)
    for x in range(1, 100):
        context.move_to(x, 0)
        context.line_to(x, 100)
        context.stroke()
    for y in range(1, 100):
        context.move_to(0, y)
        context.line_to(100, y)
        context.stroke()

@contextlib.contextmanager
def image_generator(filename, tile_edge, width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.scale(tile_edge, tile_edge)
    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0, float(width) / tile_edge, float(height) / tile_edge)
    context.fill()
    yield context
    surface.write_to_png(filename)

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks. Standard recipe."
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

if __name__ == '__main__':
    main()
