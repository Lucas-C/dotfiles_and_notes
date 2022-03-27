#!/usr/bin/env python3
"Apply a .gpl color palette to an image"
import argparse, os, re
from typing import Dict, NamedTuple, Optional, Tuple

from PIL import Image


class Palette(NamedTuple):
    name: str
    colors: Dict[str, Tuple[int]]
    columns: Optional[int] = None


def quantize_to_palette(img, palette, dither=0):
    """
    Convert an RGB or L mode image to use a given palette.
    Image.quantize source: https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.quantize
    """
    # Create a temporary image using the palette:
    pal_img = Image.new('P', (16, 16))  # size does not matter
    flat_palette = [value for color in palette for value in color]
    pal_img.putpalette(flat_palette)

    new_img = img.quantize(palette=pal_img, dither=dither)
    pal_img.close()

    new_img_palette = list(iter_triplets(new_img.palette.palette))[:len(palette)]
    assert sorted(new_img_palette) == sorted(palette), 'Resulting image does not have the expected palette'

    return new_img


def iter_triplets(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), ..."
    a = iter(iterable)
    return zip(a, a, a)


def parse_gpl_file(gpl_filepath):
    with open(gpl_filepath, encoding='utf-8') as gpl_file:
        lines = [line.strip() for line in gpl_file.readlines()]
    assert lines[0] == 'GIMP Palette'
    name = lines[1][len('Name: '):]
    columns = None
    if 'Columns: ' in lines[2]:
        columns = int(lines[2][len('Columns: '):])
        del lines[2]
    colors = {}
    for line in lines[2:]:
        if not line.startswith('#'):
            r, g, b, color = [e for e in re.split(' +|\t+', line) if e]
            colors[color] = (int(r), int(g), int(b))
    return Palette(name=name, colors=colors, columns=columns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('gpl_filepath')
    parser.add_argument('img_filepath')
    parser.add_argument('--add-palette', action='store_true', help='Display the palette at the bottom of the image')
    args = parser.parse_args()
    basename, ext = os.path.splitext(args.img_filepath)
    out_filepath = basename + '-paletted' + ext
    palette = parse_gpl_file(args.gpl_filepath)
    with Image.open(args.img_filepath) as img:
        if img.mode != 'RGB':
            new_img = Image.new('RGB', img.size, 'WHITE')
            new_img.paste(img, (0, 0), img)
            img.close()
            img = new_img
        out_img = quantize_to_palette(img, palette.colors.values())
    if args.add_palette:
        from color_palette_extract import add_palette_to_img
        out_img = add_palette_to_img(out_img)
    elif ext.lower() in ('.jpg', '.jpeg'):
        out_img = out_img.convert('RGB')
    out_img.save(out_filepath)
    out_img.close()
    print(f'{out_filepath} generated')
