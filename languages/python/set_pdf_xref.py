#!/usr/bin/env python3

# Script to re-build a PDF xref table
# once it has been manually edited

# USAGE: ./set_pdf_xref.py in.pdf [--inplace|out.pdf]

import sys


def main():
    input_filepath = sys.argv[1]
    if len(sys.argv) > 2:
        output_filepath = input_filepath if sys.argv[2] == '--inplace' else sys.argv[2]
    else:
        output_filepath = 'out-' + input_filepath
        print('Output generated to:', output_filepath)

    with open(input_filepath, 'rb') as input_file:
        data = input_file.read()

    xref_pos = data.index(b'\nxref') + 1
    startxref_start = data.index(b'\nstartxref\n') + len('\nstartxref\n')
    startxref_end = data.index(b'\n', startxref_start)
    if xref_pos != int(data[startxref_start:startxref_end]):
        data = data[:startxref_start] + str(xref_pos).encode() + data[startxref_end:]

    with open(output_filepath, 'wb') as output_file:
        output_file.write(data)

    # from pdfrw import PdfReader, PdfWriter
    # out = PdfWriter()
    # out.addpage(PdfReader(fdata=data).pages[0])
    # out.write(output_filepath)


if __name__ == '__main__':
    main()
