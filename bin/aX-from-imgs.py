#!/usr/bin/env python3
# USAGE: ./a3-from-imgs.py [--a3/4/5/6] [--landscape] [--no-margin] [--repeat-imgs] $img_file1 [$img_file2]
# Script Dependencies:
#    fpdf2
import argparse, sys
from fpdf import FPDF


def gen(args):
    if args.format == "a5":
        pdf_format = "a4"
        args.orientation = "landscape"
    elif args.format == "a6":
        pdf_format = "a4"
    else:
        pdf_format = args.format
    pdf = FPDF(format=pdf_format, orientation=args.orientation)
    if args.margin is not None:
        pdf.set_margin(args.margin)
    half_h, half_w = pdf.eph/2, pdf.epw/2
    if args.format == "a5":
        kwargs = dict(keep_aspect_ratio=True, h=pdf.eph, w=half_w)
    elif args.format == "a6":
        kwargs = dict(keep_aspect_ratio=True, h=half_h, w=half_w)
    else:
        kwargs = dict(keep_aspect_ratio=True)
    img_iterator = build_img_iterator(args)
    try:
        while True:
            first_img_on_page = next(img_iterator)
            if args.out is None:
                args.out = f"{first_img_on_page[:-4]}.pdf"
            pdf.add_page()
            if args.format == "a5":
                pdf.image(first_img_on_page, **kwargs, x=pdf.x,        y=pdf.y)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+half_w, y=pdf.y)
            elif args.format == "a6":
                pdf.image(first_img_on_page, **kwargs, x=pdf.x,        y=pdf.y)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+half_w, y=pdf.y)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x,        y=pdf.y+half_h)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+half_w, y=pdf.y+half_h)
            else:
                pdf.image(first_img_on_page,**kwargs, h=pdf.eph, w=pdf.epw)
    except StopIteration:  # raised by next(img_iterator) at some point
        pass
    pdf.output(args.out)
    print(f"{args.out} generated")


def build_img_iterator(args):
    for img_filepath in args.img_filepaths:
        yield img_filepath
        if args.repeat_imgs:
            if args.format == "a5":
                yield img_filepath
            if args.format == "a6":
                yield img_filepath
                yield img_filepath
                yield img_filepath


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     allow_abbrev=False)
    parser.add_argument("--format", default="a4")
    parser.add_argument("--a3", action="store_const", dest="format", const="a3")
    parser.add_argument("--a4", action="store_const", dest="format", const="a4")
    parser.add_argument("--a5", action="store_const", dest="format", const="a5")
    parser.add_argument("--a6", action="store_const", dest="format", const="a6")
    parser.add_argument("--orientation", choices=("landscape", "portrait"), default="portrait")
    parser.add_argument("--portrait", action="store_const", dest="orientation", const="portrait")
    parser.add_argument("--landscape", action="store_const", dest="orientation", const="landscape")
    parser.add_argument("--margin", type=float)
    parser.add_argument("--no-margin", action="store_const", dest="margin", const=0)
    parser.add_argument("--repeat-imgs", action="store_true")
    parser.add_argument("--out", help="Output file path")
    parser.add_argument("img_filepaths", nargs="+")
    args = parser.parse_args(sys.argv[1:])
    if args.repeat_imgs and args.format not in ("a5", "a6"):
        parser.error("--repeat-imgs is only meaningful with --a5/6")
    return args


if __name__ == "__main__":
    gen(parse_args())
