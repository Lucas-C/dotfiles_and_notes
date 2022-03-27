#!/usr/bin/env python3
"Extract the color palette from an image into a .gpl color palette file"
import argparse, os

from colorthief import ColorThief  # pip install colorthief
# from haishoku.haishoku import Haishoku  # alternative lib, cf. https://github.com/fengsp/color-thief-py/issues/28
from PIL import Image, ImageDraw


RADIUS = 50  # radius of the bottom palette circles
WHITE = (255, 255, 255)


def write_gpg_file(colors, name, gpl_filepath):
    with open(gpl_filepath, 'w', encoding='utf-8') as gpl_file:
        gpl_file.write('GIMP Palette\n')
        gpl_file.write(f'Name: {name}\n')
        gpl_file.write(f'Columns: {len(colors)}\n')
        gpl_file.write('#\n')
        for i, color in enumerate(colors):
            gpl_file.write(f'{" ".join(map(str, color))} Color{i}\n')


def add_palette_to_img(img, palette):
    width, height = img.size
    height += 2*RADIUS  # adds space for the palette at the bottom
    width = max(width, len(palette) * 2*RADIUS)  # if not enough width for the palette, extend the image
    pal_img = Image.new('RGB', (width, height), WHITE)
    pal_img.paste(img)
    draw = ImageDraw.Draw(pal_img)
    for i, color in enumerate(palette):
        draw.ellipse((i*2*RADIUS, height-2*RADIUS, (i+1)*2*RADIUS, height), fill=color)
    return pal_img


def iter_triplets(iterable):
    "s -> (s0, s1, s2), (s3, s4, s5), ..."
    a = iter(iterable)
    return zip(a, a, a)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--colors', type=int, default=16, help=' ')
    parser.add_argument('--algo', choices=('colorthief', 'pillow'), help=' ')
    parser.add_argument('--gen-img', action='store_true', help='Also generates an image file showing the palette')
    parser.add_argument('img_filepath')
    args = parser.parse_args()
    basename, ext = os.path.splitext(args.img_filepath)
    out_gpl_filepath = basename + '.gpl'

    if args.algo == 'pillow':
        img = Image.open(args.img_filepath)
        new_img = img.convert('P', colors=len(palette.colors), palette=Image.ADAPTIVE)
        img.close()
        img = new_img
        palette = list(iter_triplets(img.palette.palette))
        assert all(color == (0, 0, 0) for color in palette[args.colors:])
        palette = palette[:args.colors]
    else:
        color_thief = ColorThief(args.img_filepath)
        palette = color_thief.get_palette(color_count=args.colors + 1, quality=1)
        img = color_thief.image  # Pillow image opened by ColorThief

        if args.gen_img:  # we convert the image by one indexed by this color palette
            # Create a temporary image using the palette:
            pal_img = Image.new('P', (16, 16))  # size does not matter
            flat_palette = [value for color in palette for value in color]
            pal_img.putpalette(flat_palette)

            new_img = img.quantize(palette=pal_img)
            pal_img.close()

            new_img_palette = list(iter_triplets(new_img.palette.palette))[:len(palette)]
            assert sorted(new_img_palette) == sorted(palette), 'Resulting image does not have the expected palette'

            img.close()
            img = new_img

    assert len(palette) == args.colors
    palette_name = f'{args.colors}-colors palette from {args.img_filepath}'
    write_gpg_file(palette, palette_name, out_gpl_filepath)
    print(f'{out_gpl_filepath} generated')
    if args.gen_img:
        pal_img = add_palette_to_img(img, palette)
        out_filepath = basename + '-with-palette' + ext
        out_filepath = basename + '-with-palette.png'  # tmp test
        pal_img.save(out_filepath)
        pal_img.close()
        print(f'{out_filepath} generated')
    img.close()
