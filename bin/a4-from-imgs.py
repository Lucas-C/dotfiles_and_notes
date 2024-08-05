#!/usr/bin/env python3
# USAGE: ./a4-from-imgs.py [--landscape] [--no-margin] $img_file1 $img_file2
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
    for img_path in args:
        pdf.add_page()
        pdf.image(img_path, h=pdf.eph, w=pdf.epw, keep_aspect_ratio=True)
    out_filepath = f"{args[0][:-4]}.pdf"
    pdf.output(out_filepath)
    print(f"{out_filepath} generated")

gen(sys.argv[1:])
