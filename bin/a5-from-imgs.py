#!/usr/bin/env python3
# USAGE: ./a5-from-imgs.py [--landscape] [--no-margin] $img_file1 $img_file2
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
    half_w = pdf.epw/2
    kwargs = dict(h=pdf.eph, w=half_w, keep_aspect_ratio=True)
    for img_path1, img_path2 in pairs(args):
        pdf.add_page()
        pdf.image(img_path1, **kwargs, x=pdf.x,        y=pdf.y)
        pdf.image(img_path2, **kwargs, x=pdf.x+half_w, y=pdf.y)
    out_filepath = f"{args[0][:-4]}-flyers-a5.pdf"
    pdf.output(out_filepath)
    print(f"{out_filepath} generated")

def pairs(img_paths):
    for k in range((len(img_paths)+1)//2):
        i, j = 2*k, 2*k+1
        yield (img_paths[i], img_paths[j] if j < len(img_paths) else img_paths[i])

gen(sys.argv[1:])
