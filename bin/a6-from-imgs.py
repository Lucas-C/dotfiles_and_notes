#!/usr/bin/env python3
# USAGE: ./a6-from-imgs.py [--landscape] [--no-margin] $img_file1 $img_file2
# Script Dependencies:
#    fpdf2
import sys
from fpdf import FPDF

def gen(args):
    orientation = "portrait"
    if args[0] == "--landscape":
        args = args[1:]
        orientation = "landscape"
    pdf = FPDF(orientation=orientation)
    if args[0] == "--no-margin":
        args = args[1:]
        pdf.set_margin(0)
    half_h, half_w = pdf.eph/2, pdf.epw/2
    kwargs = dict(h=half_h, w=half_w, keep_aspect_ratio=True)
    for img_path in args:
        pdf.add_page()
        pdf.image(img_path, **kwargs, x=pdf.x,        y=pdf.y)
        pdf.image(img_path, **kwargs, x=pdf.x+half_w, y=pdf.y)
        pdf.image(img_path, **kwargs, x=pdf.x,        y=pdf.y+half_h)
        pdf.image(img_path, **kwargs, x=pdf.x+half_w, y=pdf.y+half_h)
    out_filepath = f"{args[0][:-4]}-flyers-a6.pdf"
    pdf.output(out_filepath)
    print(f"{out_filepath} generated")

gen(sys.argv[1:])
