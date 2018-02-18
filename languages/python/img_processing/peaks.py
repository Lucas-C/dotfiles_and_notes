#!/usr/bin/python3

# Original code by vvdr12: https://gist.github.com/vvdr12/7310160
# USAGE: ./peaks.py zSLuUZ9.jpg
# REQUIRE: Pillow + optionally tqdm

# TODO: generate a GIF !

import argparse
from PIL import Image
from os.path import basename, dirname, join
try:
    from tqdm import tqdm
except ImportError:  # optional dependency, simply print a X/Y ratio on each step else
    def tqdm(iterable, total):  # fallback
        for j, _ in enumerate(iterable):
            if j % 100 == 0: yield print(f'{j} / {total}')


def main():
    args = parse_args()
    destination_image = join(dirname(args.source_image),
                             'japanified_' + basename(args.source_image))

    img = Image.open(args.source_image)
    print('Format:', img.format)
    print('Size:', img.size)
    print('Mode:', img.mode)

    img_height = img.size[1]
    rows_spacing = args.rows_spacing if args.rows_spacing else img_height // 100
    peaks(img, rows_spacing)
    img.save(destination_image)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_image')
    parser.add_argument('--rows-spacing', type=int, default=0,
                        help='change for higher/lower line density')
    return parser.parse_args()


def peaks(img, rows_spacing):
    width, height = img.size
    img = img.load()  # getting PixelAccess
    print('# Phase 1')
    points = list(tqdm(phase_1(img, width, height, rows_spacing), total=height // rows_spacing))
    print('# Phase 2')
    list(tqdm(phase_2(img, height, points, rows_spacing), total=len(points)))


def phase_1(img, width, height, rows_spacing):
    scale = 1
    j = rows_spacing
    for j in range(rows_spacing, height, rows_spacing):
        row_points = []
        iold = 0
        jold = j
        for i in range(width):
            altitude = sum(img[i, j][:3]) / 3
            if altitude > 0:
                altitude = (altitude * altitude) / 2000

            inew = int(i * scale)
            jnew = int((j - altitude) * scale)

            if jnew > 0:
                row_points.append([inew, jnew])

            di = inew - iold
            dj = jnew - jold
            length = max(abs(di), abs(dj))
            for k in range(0, length):
                icurrent = round(k * di / length) + iold
                jcurrent = round(k * dj / length) + jold
                if jcurrent >= 0:
                    img[icurrent, jcurrent] = (100, 100, 100)
                    row_points.append([icurrent, jcurrent])

            iold = inew
            jold = jnew
        yield row_points


def phase_2(img, height, points, rows_spacing):
    # clear overlaps then re-write line
    for k in range(0, len(points)):
        for l in range(0, len(points[k])):
            i = points[k][l][0]
            j = points[k][l][1]
            j0 = rows_spacing * (k + 1)
            dj = abs(j - j0)
            for m in range(0, dj):
                if (j + m) < height:
                    img[i, j + m] = (240, 240, 240)
        for l in range(0, len(points[k])):
            i = points[k][l][0]
            j = points[k][l][1]
            if l == 0:
                j0 = j
            dj = abs(j - j0) * 10
            img[i, j] = (100, 100, 100)
        yield 'progress tracking'


if __name__ == '__main__':
    main()
