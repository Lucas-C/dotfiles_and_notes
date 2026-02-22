#!/usr/bin/env python3
# USAGE: ./a3-from-imgs.py [--a3/4/5/6] [--landscape/portrait] [--margin=X] [--padding=X] [--repeat-imgs] $img_file1 [$img_file2]
# Script Dependencies:
#    fpdf2
import argparse, pathlib, sys
from itertools import count
from fpdf import FPDF
from fpdf.enums import PageOrientation
from fpdf.image_parsing import preload_image


def gen(args):
    if args.format == "a5":
        pdf_format = "a4"
        if not args.orientation:
            args.orientation = "landscape"
    elif args.format == "a6":
        pdf_format = "a4"
    else:
        pdf_format = args.format
    pdf = FPDF(format=pdf_format, orientation=args.orientation or "portrait")
    pdf.set_margin(args.margin)
    half_h, half_w = pdf.eph/2, pdf.epw/2
    kwargs = {"keep_aspect_ratio": not args.stretch}
    if args.format == "a5":
        if args.orientation == "landscape":
            kwargs["h"] = pdf.eph - 2*args.padding
            kwargs["w"] = half_w - 2*args.padding
        else:
            kwargs["h"] = half_h - 2*args.padding
            kwargs["w"] = pdf.epw - 2*args.padding
    elif args.format == "a6":
        kwargs["h"] = half_h - 2*args.padding
        kwargs["w"] = half_w - 2*args.padding
    else:
        kwargs["h"] = pdf.eph - 2*args.padding
        kwargs["w"] = pdf.epw - 2*args.padding
    img_iterator = build_img_iterator(args)
    try:
        for index in count(1):
            first_img_on_page = next(img_iterator)
            if not args.orientation:
                _name, _img, info = preload_image(pdf.image_cache, first_img_on_page)
                orientation = PageOrientation.LANDSCAPE if info["w"] > info["h"] else PageOrientation.PORTRAIT
                print(f"Auto-detected document orientation for page {index}: {orientation.name}")
                if orientation != pdf.cur_orientation:
                    pdf._set_orientation(orientation, pdf.dw_pt, pdf.dh_pt)
                    pdf.def_orientation = pdf.cur_orientation
                    kwargs["h"], kwargs["w"] = kwargs["w"], kwargs["h"]
            if args.out is None:
                args.out = first_img_on_page.with_suffix(".pdf")
                if args.suffix:
                    args.out = args.out.with_stem(args.out.stem + f"-{args.suffix}")
            pdf.add_page()
            if args.format == "a5":
                pdf.image(first_img_on_page, **kwargs,  x=pdf.x+args.padding,        y=pdf.y+args.padding)
                if pdf.cur_orientation == PageOrientation.LANDSCAPE:
                    pdf.image(next(img_iterator), **kwargs, x=pdf.x+args.padding+half_w, y=pdf.y+args.padding)
                else:
                    pdf.image(next(img_iterator), **kwargs, x=pdf.x+args.padding, y=pdf.y+args.padding+half_h)
            elif args.format == "a6":
                pdf.image(first_img_on_page, **kwargs,  x=pdf.x+args.padding,        y=pdf.y+args.padding)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+args.padding+half_w, y=pdf.y+args.padding)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+args.padding,        y=pdf.y+args.padding+half_h)
                pdf.image(next(img_iterator), **kwargs, x=pdf.x+args.padding+half_w, y=pdf.y+args.padding+half_h)
            else:
                pdf.image(first_img_on_page,**kwargs, x=pdf.x+args.padding, y=pdf.y+args.padding)
    except StopIteration:  # raised by next(img_iterator) at some point
        pass
    pdf.output(args.out)
    print(f"{args.out} generated with {index - 1} pages")


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
    parser.add_argument("--orientation", choices=("landscape", "portrait"))
    parser.add_argument("--portrait", action="store_const", dest="orientation", const="portrait")
    parser.add_argument("--landscape", action="store_const", dest="orientation", const="landscape")
    parser.add_argument("--margin", type=float, default=0, help="Outer page margin")
    parser.add_argument("--padding", type=float, default=0, help="Inner image padding")
    parser.add_argument("--repeat-imgs", action="store_true")
    parser.add_argument("--stretch", action="store_true")
    parser.add_argument("--out", "-o", type=pathlib.Path, help="Output file path. Default to the input file name with the extension replaced to .pdf")
    parser.add_argument("--suffix", help="Suffix to append to the output file name")
    parser.add_argument("img_filepaths", nargs="+", type=pathlib.Path)
    args = parser.parse_args(sys.argv[1:])
    if args.repeat_imgs and args.format not in ("a5", "a6"):
        parser.error("--repeat-imgs is only meaningful with --a5/6")
    if args.out and args.suffix:
        print("WARNING: --out & --suffix both provided, --suffix is ignored")
        args.suffix = None
    return args


if __name__ == "__main__":
    gen(parse_args())
