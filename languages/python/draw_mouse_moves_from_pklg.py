#!/usr/bin/env python

# Utilisé dans le cadre d'un CTF où il fallait parser des trames Bluetooth HID d'une souris Apple Mouse

import cairo, json, math
from collections import Counter


def main():
    with open('dump-from-wireshark.json') as json_dump_file:
        packets = json.load(json_dump_file)
    btl2cap_packets = [p["_source"]["layers"]["btl2cap"] for p in packets if p["_source"]["layers"].get("btl2cap")]
    print('# L2CPAP packet:', len(btl2cap_packets))
    btl2cap_payloads = [p["btl2cap.payload"] for p in btl2cap_packets]
    payload_lengths = Counter(len(p) for p in btl2cap_payloads)
    print('Packet count per payload length:', payload_lengths)
    payload_prefixes = Counter(p[:9] for p in btl2cap_payloads)
    print('Packet count per prefix:', payload_prefixes)
    moves = [extract_move(payload) for payload in btl2cap_payloads]
    draw_moves(moves, 'moves.png')

def extract_move(payload):
    data = payload.split(':')
    x = int(data[3], 16) | (int(data[4], 16) << 8)
    if x > 2**15:
        x -= 2**16
    y = int(data[5], 16) | (int(data[6], 16) << 8)
    if y > 2**15:
        y -= 2**16
    return x, y

def draw_moves(moves, png_filepath):
    if len(moves) <= 1:
        return
    moves = list(relativize(moves))
    minX = min(pos[0] for pos in moves)
    maxX = max(pos[0] for pos in moves)
    minY = min(pos[1] for pos in moves)
    maxY = max(pos[1] for pos in moves)
    roundedMinXY = 10 * math.floor(min(minX, minY) / 10)
    roundedMaxXY = 10 * math.ceil(max(maxX, maxY) / 10)
    size = roundedMaxXY - roundedMinXY
    print('#moves: {} - minX: {} - maxX: {} - minY: {} - maxY: {} - size: {}'.format(len(moves), minX, maxX, minY, maxY, size))
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
    context = cairo.Context(surface)
    context.fill()
    context.set_source_rgb(1, 1, 1)
    context.set_line_width(1)
    moved = False
    for pos in moves:
        new_pos = (pos[0] - roundedMinXY, pos[1] - roundedMinXY)
        if moved:
            context.line_to(*new_pos)
            context.stroke()
        context.move_to(*new_pos)
        moved =True
    if moved:
        context.line_to(*new_pos)
        context.stroke()
    surface.write_to_png(png_filepath)

def relativize(moves):
    x, y = 0, 0
    for m in moves:
        x += m[0]
        y += m[1]
        yield x, y

if __name__ == '__main__':
    main()
