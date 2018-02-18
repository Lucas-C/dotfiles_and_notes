#!/usr/bin/python3

# Original code by vvdr12: https://gist.github.com/vvdr12/6327611
# USAGE: ./japanify.py TDZSJMs.jpg
# REQUIRE: Pillow + optionally tqdm

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
    list(tqdm(japanify(img, args.threshold), total=img_height))
    img.save(destination_image)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_image')
    parser.add_argument('--threshold', type=int, default=20,
                        help='change for higher/lower line density')
    return parser.parse_args()


def japanify(img, threshold):
    width, height = img.size
    img = img.load()  # getting PixelAccess
    for j in range(height):
        contrast = contrastpoints(img, j - 1 if j else 0, width, threshold) # computing contrast of previous row
        m = 0
        for i in range(width):
            if m < len(contrast) and i >= contrast[m]:
                img[i, j] = (0, 0, 0) # black
                m += 1
        yield 'ROW_COMPLETE' # progress tracking


def contrastpoints(img, j, width, threshold):
    contrast = []
    for i in range(width - 3):
        ave1 = sum(img[i + 0, j][:3]) / 3
        ave2 = sum(img[i + 1, j][:3]) / 3
        ave3 = sum(img[i + 2, j][:3]) / 3
        ave4 = sum(img[i + 3, j][:3]) / 3
        if abs(ave2 - ave1) > threshold and  abs(ave1 - ave3) > (threshold / 2):
            contrast.append(i)
    return contrast


if __name__ == '__main__':
    main()
