#!/usr/bin/env python3

# Script to re-build a PDF xref table
# once it has been manually edited

# USAGE: ./set_pdf_xref.py in.pdf [out.pdf]

import sys
from pdfrw import PdfReader, PdfWriter


def main():
    input_filepath = sys.argv[1]
    print(input_filepath)
    output_filepath = sys.argv[2] if len(sys.argv) > 2 else 'out-' + input_filepath

    with open(input_filepath, 'rb') as input_file:
        data = input_file.read()

    xref_pos = data.index(b'\nxref') + 1
    startxref_start = data.index(b'\nstartxref\n') + len('\nstartxref\n')
    startxref_end = data.index(b'\n', startxref_start)
    if xref_pos != int(data[startxref_start:startxref_end]):
        data = data[:startxref_start] + str(xref_pos).encode() + data[startxref_end:]

    out = PdfWriter()
    out.addpage(PdfReader(fdata=data).pages[0])
    out.write(output_filepath)


if __name__ == '__main__':
    main()
