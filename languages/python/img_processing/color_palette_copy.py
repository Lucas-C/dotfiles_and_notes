#!/usr/bin/env python3
"Copy the palette from one image to another"
import argparse, os

from PIL import Image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('paletted_filepath')
    parser.add_argument('img_filepath')
    parser.add_argument('--colors', type=int, default=256)
    parser.add_argument('--add-palette', action='store_true', help='Display the palette at the bottom of the image')
    args = parser.parse_args()

    basename, ext = os.path.splitext(args.img_filepath)
    out_filepath = basename + '-paletted.png'

    palette_img = Image.open(args.paletted_filepath)
    if palette_img.mode != 'P':
        palette_img = palette_img.convert('P', colors=args.colors, palette=Image.Palette.ADAPTIVE)

    img = Image.open(args.img_filepath)
    if img.mode != 'RGB':
        new_img = Image.new('RGB', img.size, 'WHITE')
        new_img.paste(img, (0, 0), img)
        img = new_img

    img = img.quantize(palette=palette_img, dither=0)

    if args.add_palette:
        from color_palette_extract import add_palette_to_img
        img = add_palette_to_img(img)
    elif ext.lower() in ('.jpg', '.jpeg'):
        out_img = out_img.convert('RGB')

    img.save(out_filepath)
    print(f'{out_filepath} generated')
