#!/usr/bin/python3

# Idea from vvdr12: https://www.reddit.com/r/glitch_art/comments/1p5mno/elephant_hill/ccyzbn1/
# USAGE: ./steal_colors_with_same_brightness.py --palette-img edJl3YU.jpg japanified_TDZSJMs.jpg
# REQUIRE: Pillow + optionally tqdm

import argparse
from bisect import bisect_left # binary/dichotomic search on lists
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
                             'colorstolen_' + basename(args.source_image))

    img = Image.open(args.source_image)
    print('Format:', img.format)
    print('Size:', img.size)
    print('Mode:', img.mode)

    steal_colors(img, args.palette_img)
    print('Writing to:', destination_image)
    img.save(destination_image)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_image')
    parser.add_argument('--palette-img', required=True)
    return parser.parse_args()


def steal_colors(img, palette_img_src):
    print('# Building replacement palette')
    palette = Palette(palette_img_src, brightness_func=luminosity)

    print('# Subsituting colors')
    img_height = img.size[1]
    list(tqdm(subst_img_colors(img, palette, brightness_func=luminosity), total=img_height))


class Palette():
    def __init__(self, palette_img_src, brightness_func):
        self.palette = {}
        with Image.open(palette_img_src) as palette_img:
            palette_img_height = palette_img.size[1]
            list(tqdm(self._build_palette(palette_img, brightness_func), total=palette_img_height))
        print('Palette size:', len(self.palette))
        self.sorted_keys = sorted(self.palette.keys())
    def _build_palette(self, palette_img, brightness_func):
        width, height = palette_img.size
        palette_pixels = palette_img.load()  # getting PixelAccess
        for j in range(height):
            for i in range(width):
                brightness = brightness_func(palette_pixels[i, j])
                self.palette[brightness] = palette_pixels[i, j] # nothing smart (ex: avg): we only keep the last brightness value processed
            yield 'ROW_COMPLETE' # progress tracking
    def __getitem__(self, key):
        i = bisect_left(self.sorted_keys, key)  # O(logN)
        brightness = max(self.sorted_keys) if i == len(self.sorted_keys) else self.sorted_keys[i]
        return self.palette[brightness]


def subst_img_colors(img, luminosity2color_palette, brightness_func):
    width, height = img.size
    img = img.load()  # getting PixelAccess
    for j in range(height):
        for i in range(width):
            img[i, j] = luminosity2color_palette[brightness_func(img[i, j])]
        yield 'ROW_COMPLETE' # progress tracking


def luminosity(pixel):
    if len(pixel) > 3 and not pixel[3]:
        return 0  # transparent
    r, g, b = pixel[:3]
    return 0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)


if __name__ == '__main__':
    main()
